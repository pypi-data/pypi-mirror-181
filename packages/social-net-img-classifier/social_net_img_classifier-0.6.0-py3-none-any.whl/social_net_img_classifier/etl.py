import json
import random
import re
import requests
import traceback
import uuid

import pandas as pd
import numpy as np
import reverse_geocoder as rg
from statistics import mode
from datetime import date, datetime, timedelta
from io import BytesIO
from PIL import Image
from fuzzywuzzy import fuzz
import nltk
from multiprocessing import Process, Manager, cpu_count

from wj_social_net_queries.core.instagram import Instagram
from wj_social_net_queries.core.twitter import Twitter
from social_net_img_classifier.aws_utils import AwsS3
from social_net_img_classifier.classify import ClassifyImg, ClassifyNudity, ClassifySTTM, ClassifyText, OpenAI
from social_net_img_classifier.db_tools import MySQLtools
from social_net_img_classifier.utils import GenderByText, NlpUtils, CalcUtils, Location
from social_net_img_classifier.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, BRANDS, BUCKET_NAME, BUSINESS_NAME_WORDS, CHECK_NUDITY,\
    COUNTRIES, DAYS_LIMIT, GREETINGS, IG_BUSINESS_CATEGORY, IG_CATEGORY, IMG_DB_FIELDS, IG_TOKEN, LANGUAGES, LOCATIONS,\
    MAX_TWEETS_PER_TERM, OPENAI_CLF, SCAN_IMAGES, RESPONSE_TWEETS, TEMPLATES_DM_DIR, TEMPLATES_RP_DIR, TERMS, TW_CONN

DATE_COL = "date"
TARGET = "target"

KEYS = {
    "images": ["filename"],
    "tweets": ["tweet_id"],
    "words": ["source", DATE_COL, "country_iso2", "admin1", "word"],
    "report_tw": ["id"],
}

TW_TERMS = [x.lower() for x in TERMS["twitter"] + BRANDS["twitter"]]
IG_TERMS = TERMS["instagram"]

TEMPLATES_DM = list(pd.read_json(AwsS3().read_file(TEMPLATES_DM_DIR))["text"])
TEMPLATES_RP = pd.read_json(AwsS3().read_file(TEMPLATES_RP_DIR))


class MainETL:
    """
    :Date: 2022-12-14
    :Version: 1.8
    :Author: Joan Felipe Mendoza - Whale & Jaguar Consultants S.A.S.
    :Description: PIPELINE PRINCIPAL
    """
    def __init__(self) -> None:
        try:
            nltk.download('stopwords')
            nltk.download('wordnet')
            nltk.download('punkt')
            nltk.download('cmudict')
            print("NLTK packages downloaded")
        except Exception:
            print("NLTK packages already downloaded")
            pass

    def execute_ig(self, terms=IG_TERMS, locations=LOCATIONS, s3_raw_path="raw", s3_dest_path="processed"):
        """
        :Description: ejecutar pipeline sobre AWS
        :param terms: términos a buscar en Instagram (:type: list)
        :param locations: locaciones a buscar en Instagram (:type: list)
        :param s3_raw_path: ubicación original (:type: string)
        :param s3_dest_path: ubicación de destino (:type: string)
        :return: lista de usuarios a contactar (:type: dict)
        """
        # Descargar datos desde Instagram y almacenar en S3
        IngestData.instagram_locations_to_S3(locations)
        IngestData.instagram_terms_to_S3(terms)
        # Derivar variables desde datos almacenados en S3
        data, json_processed = self.derive_ig_from_S3()
        # Cargar a base de datos
        success = MySQLtools(table="images").update_table(data, KEYS["images"], batch=100)
        # Mover archivos procesados a sus carpetas correspondientes
        users = {}
        if success:
            _ = [AwsS3().copy_delete_file(file, f"processed/{file}") for file in json_processed]
        if len(data):
            data1 = data[data[TARGET] == 1]
            pred0 = list(data[data[TARGET] == 0]["filename"])
            pred1 = list(data1["filename"])
            _ = [AwsS3().copy_delete_file(f"{s3_raw_path}/{f}", f"{s3_dest_path}/no_moment/{f}") for f in pred0]
            _ = [AwsS3().copy_delete_file(f"{s3_raw_path}/{f}", f"{s3_dest_path}/is_moment/{f}") for f in pred1]
            # Calcular lista de usuarios a contactar
            true_cases = data[
                (data[TARGET] == 1) & (data["profile_type"] == "person") & (data["country_iso2"].isin(COUNTRIES))
                ]
            users = true_cases[["owner_id", "owner_username"]].drop_duplicates().to_dict("records")
        return users

    def execute_tw(self, terms=TW_TERMS, max_tweets=MAX_TWEETS_PER_TERM, batch=240):
        # Descargar datos desde Twitter y almacenar en DB
        tweets_data, _ = IngestData.twitter(terms=terms, max_tweets=max_tweets, update_db=True)
        # Calcular lista de usuarios a contactar
        query = f"SELECT tweet_id, screen_name, twitter_id, created_at, `text`, place, lang, media_url_https, " \
                f"user_description, user_name, user_location, verified FROM tweets WHERE target IS NULL LIMIT {batch}"
        while len(tweets_data) > 0:
            start = datetime.now()
            # Simular descarga de datos desde streaming
            tweets_data = MySQLtools().read_mysql_df(query=query)
            # Derivar datos
            tweets_data, contacts = self.process_batch_tw(tweets_data)
            # Almacenar datos en MySQL
            _ = MySQLtools(table="tweets").update_table(tweets_data, KEYS["tweets"], batch=batch)
            # Enviar mensajes directos a usuarios
            responses = Responding().twitter(contacts)
            _ = MySQLtools(table="report_tw").update_table(responses, KEYS["report_tw"], batch=batch)
            print(f"Tiempo de proceso: {datetime.now() - start}")

    def process_batch_tw(self, tweets_data):
        """
        Procesar en conversaciones en bache.
        :param tweets_data: conversaciones a procesar (:type: list[dict] or pandas.DataFrame)
        :return:
                data: datos procesados (:type: pandas.DataFrame)
                contacts: lista de usuarios a contactar (:type: list[dict])
        """
        # Descargar datos desde Twitter y almacenar en DB
        start = datetime.now()
        contacts = {}
        data = pd.DataFrame()
        lng = len(tweets_data)
        print("***")
        if lng:
            # Derivar
            tweets_data = pd.DataFrame(tweets_data).drop_duplicates(subset=["tweet_id"]).to_dict("records")
            tweets_data = self.multiprocess(target_method=self.transform_data, data=tweets_data)
            tweets_data = pd.DataFrame(tweets_data)
            data = tweets_data[tweets_data["country_iso2"].isin(COUNTRIES)].to_dict("records")
            data = self.derive_tw(data)
            # Calcular lista de usuarios a contactar
            if data.shape[0]:
                true_cases = data[(data[TARGET] == 1) & (data["gender"].isin(["M", "F"])) & (data["verified"] == 0)]
                contacts = true_cases[["screen_name", "twitter_id", "user_name", "tweet_id", "sttm_group"]].to_dict("records")
            data_0 = tweets_data[~tweets_data["country_iso2"].isin(COUNTRIES)]
            data_0[TARGET] = [-1] * len(data_0)  # Inicializar como No predecido
            data = pd.concat([data, data_0], axis=0).reset_index(drop=True)
        end = datetime.now()
        print(f"**Total time** {end - start}\n"
              f"**Records** {lng}\n"
              f"**Avg time per record** {(end - start) / lng if lng else 0}\n***\n")
        return data, contacts

    @staticmethod
    def derive_tw(tweets_data, model_type="bert"):
        if len(tweets_data):
            df = pd.DataFrame(tweets_data)
            # Clasificar conversaciones por texto
            start = datetime.now()
            if model_type == "bert":
                df["target_text"] = ClassifyText(model_type=model_type).predict(df["text"], clean_mode=None)
            else:
                df["target_text"] = ClassifyText(model_type=model_type).predict(df["clean_text"], clean_mode=None)
            print(f"*Moment Clf total time* {datetime.now() - start}")
            start = datetime.now()
            obj_list, top_list, color_list, img_list, target_list, safe_list = [], [], [], [], [], []
            imgs, imgs_nudity = 0, 0
            for _, row in df.iterrows():
                # Clasificar conversaciones por imágenes
                obj_img, top_labels, color_img, target_img, safe = {}, {}, {}, -1, 1
                urls = row["media_url_https"] if row["media_url_https"] else []
                img_url = urls[0] if urls else None
                # Escanear sólo las que están en territorios a explorar
                if row["country_iso2"] in COUNTRIES:
                    for url in urls:
                        img_url = url
                        # Revisar si hay desnudez
                        if CHECK_NUDITY and safe == 1:
                            safe = ClassifyNudity(url).predict()
                            imgs_nudity += 1
                        # Escanear sólo las que no dieron positivas por texto
                        if SCAN_IMAGES and row["target_text"] == 0 and target_img < 1 and safe == 1:
                            tw_img = ClassifyImg(url)
                            color_img = tw_img.colors
                            target_img, obj_img, top_labels = tw_img.predict()
                            imgs += 1
                obj_list.append(obj_img)
                top_list.append(top_labels)
                color_list.append(color_img)
                img_list.append(img_url)
                target_list.append(target_img)
                safe_list.append(safe)
            df["obj_img"] = obj_list
            df["top_labels"] = top_list
            df["color_img"] = color_list
            df["img_url"] = img_list
            df["target_img"] = target_list
            df["safe"] = safe_list
            target_list = []
            for _, row in df.iterrows():
                target = 0
                if max(row["target_img"], row["target_text"]) == 1 and row["safe"] == 1:  # Si es un caso positivo...
                    if OpenAI().filter_content(str(row["text"])) == "0":  # Si el texto no es inapropiado...
                        target = OpenAI().clf_moment(row["text"]) if OPENAI_CLF else 1
                target_list.append(target)
            df[TARGET] = target_list
            end = datetime.now()
            print(f"*Image Clf total time* {end - start}\n"
                  f"*Images moment check* {imgs}\n"
                  f"*Images nudity check* {imgs_nudity}\n"
                  f"*Avg time per image* {(end - start) / max(imgs, imgs_nudity) if max(imgs, imgs_nudity) else 0}")
            start = datetime.now()
            df["sttm_group"] = None
            df_1 = df[df[TARGET] == 1]
            if df_1.shape[0]:
                df_0 = df[df[TARGET] != 1]
                df_1["sttm_group"] = ClassifySTTM().predict(list(df_1["text"]))
                df = pd.concat([df_1, df_0], axis=0).reset_index(drop=True)
            print(f"*STTM group total time* {datetime.now() - start}")
        else:
            df = pd.DataFrame()
        return df

    @staticmethod
    def multiprocess(target_method, data):
        output = []
        process_manager = Manager()
        return_data = process_manager.dict()
        print(f"Number of CPUs :: {cpu_count()}")
        cpu_number = cpu_count()
        jobs = []
        divide_array = np.array_split(data, cpu_number)
        for i in range(len(divide_array)):
            p = Process(target=target_method, args=(divide_array[i], return_data, i))
            jobs.append(p)
            p.start()
        for process in jobs:
            process.join()
        for array in return_data.values():
            output += array
        return output

    def transform_data(self, data, return_data, index):
        print(f"DATA Size :: {len(data)}")
        data_from_tw = []
        for json_data in data:
            text = str(json_data["text"])
            loc_fields = {"place": True, "user_location": True, "text": True}
            locations, city, country = self.location_from_text(json_data, loc_fields)
            brands = self.terms_detection(text, BRANDS["twitter"])
            if len(brands) > 0 and country is None:
                country = "CO"
            screen_name, full_name, description, gender = None, None, None, None
            clean_text, keywords, top_keyword = None, [], None
            if "screen_name" in json_data:
                screen_name = json_data["screen_name"]
            if "user_name" in json_data:
                full_name = json_data["user_name"]
            if "user_description" in json_data:
                description = json_data["user_description"]
            if country in COUNTRIES:
                clean_text = NlpUtils().clean_text(text)
                keywords = self.terms_detection(text, TERMS["twitter"])
                kwrds = brands + keywords
                top_keyword = kwrds[0] if kwrds else None
                gender = GenderByText(screen_name, full_name, description, text).predict()
            data = {
                **json_data,
                "date": str(json_data["created_at"])[:10],
                "clean_text": clean_text,
                "locations": locations,
                "city": city,
                "country_iso2": country,
                "gender": gender,
                "brands": brands,
                "keywords": keywords,
                "top_keyword": top_keyword,
            }
            data_from_tw.append(data)
        key = "process_" + str(index)
        return_data[key] = data_from_tw

    def derive_ig_from_S3(self, folder="raw"):
        """
        :Description: ejecutar proceso de detivación de variables conectándose a AWS S3
        :param folder: carpeta dentro de S3 donde están los archivos sin procesar
        :return: tabla con variables derivadas, archivos JSON que fueron procesados.
        """
        # Leer archivos JSON que contienen metadata
        json_files = AwsS3().files_in_folder(folder=folder, search_term=".json")
        metadata = []
        for file in json_files:
            try:
                d = AwsS3().read_file(file)
                metadata += json.loads(d)
            except Exception:
                print(f"Problemas leyendo '{file}'")
        output = []
        # Detectar publicaciones que ya fueron procesadas
        query = "SELECT DISTINCT shortcode FROM images WHERE shortcode IS NOT NULL"
        result = MySQLtools().read_mysql_df(query)
        if "shortcode" in result:
            processed_ids = list(result["shortcode"])
        else:
            processed_ids = []
        for json_data in metadata:
            data_from_images, processed_ids = self.read_json_instagram(json_data, folder, processed_ids)
            if data_from_images not in [None, []]:
                output += data_from_images
        return pd.DataFrame(output), json_files

    def read_json_instagram(self, json_data, folder, processed_shortcodes=None):
        """
        :Description: leer información desde un JSON generado en RapidAPI
        :param json_data: metadata generada desde RapidAPI (:type: dict)
        :param folder: carpeta que contiene imágenes u otros archivos relacionados con metadata (:type: string)
        :param processed_shortcodes: shortcodes que fueron procesados anteriormente (:type: list)
        :return: datos transformados, lista de shortcodes procesados
        """
        if processed_shortcodes is None:
            ids = []
        else:
            ids = processed_shortcodes.copy()
        data_from_images = []
        if json_data is None:
            print("No hay datos")
            return data_from_images, ids
        shortcode = json_data["code"] if "code" in json_data else None
        if not shortcode:
            print("Formato incorrecto")
            return data_from_images, ids
        if shortcode not in ids:
            post_id = json_data["pk"]
            timestamp = datetime.strptime("1970-01-01 00:00:00", "%Y-%m-%d %H:%M:%S") + timedelta(
                seconds=json_data["taken_at"])
            date = str(timestamp)[:10]
            capt = json_data["caption"] if "caption" in json_data else None
            caption, clean_text = None, None
            if isinstance(capt, dict):
                caption = capt["text"] if "text" in capt else None
                clean_text = NlpUtils().clean_text(str(caption)) if caption else None
            owner_id = json_data["owner"]["pk"]
            owner_username = json_data["owner"]["username"]
            owner_full_name = json_data["owner"]["full_name"]
            location = json_data["location"] if "location" in json_data else None
            location_lat, location_lng, location_name = None, None, None
            gender = GenderByText(user_name=owner_username, full_name=owner_full_name).predict()
            business_cn = json_data["business_category_name"] if "business_category_name" in json_data else None
            category_cn = json_data["category_name"] if "category_name" in json_data else None
            profile_type = self.ig_profile_type(business_cn, category_cn, gender, owner_full_name)
            if isinstance(location, dict):
                location_lat = location["lat"] if "lat" in location else None
                location_lng = location["lng"] if "lng" in location else None
                location_name = location["name"] if "name" in location else None
            # Obtener información geográfica
            city, admin1, admin2, country_iso2 = None, None, None, None
            if location_lat and location_lng:
                location_data = rg.search((location_lat, location_lng))[0]
                city = location_data["name"]
                admin1 = location_data["admin1"]
                admin2 = location_data["admin2"]
                country_iso2 = location_data["cc"]
            brands = self.terms_detection(caption, BRANDS["instagram"])
            keywords = self.terms_detection(caption, TERMS["instagram"])
            kwrds = brands + keywords
            top_keyword = kwrds[0] if kwrds else None
            if len(brands) > 0 and country_iso2 is not None:
                country_iso2 = "CO"
            images = AwsS3().files_in_folder(folder=folder, search_term=shortcode)
            if not len(images):
                print(f"No hay imágenes en el bucket S3 para shortcode {shortcode}")
                if "image_versions2" in json_data:
                    images = [json_data["image_versions2"]["candidates"][0]["url"]]
                elif "carousel_media" in json_data:
                    images = [x["image_versions2"]["candidates"][0]["url"] for x in json_data["carousel_media"]]
                else:
                    print(f"No hay URLs de imágenes en metadata para shortcode {shortcode}")
                    images = []
            for filename in images:
                try:
                    if filename[:4] == "http":
                        response = requests.get(filename)
                        image = BytesIO(response.content)
                        f_name = re.sub(r"^.+/", "", re.sub(r"\?.+", "", filename))
                    else:
                        image = BytesIO(AwsS3().read_file(filename))
                        f_name = filename.replace(f"{folder}/", "")
                    image = Image.open(image)
                    ig_img = ClassifyImg(image)
                    target_img, obj_img, top_labels = ig_img.predict()
                    data = {
                        "filename": f_name,
                        "id": post_id,
                        "permalink": f"https://www.instagram.com/p/{shortcode}/",
                        "shortcode": shortcode,
                        "timestamp": str(timestamp),
                        "date": date,
                        "caption": caption,
                        "clean_text": clean_text,
                        "owner_id": owner_id,
                        "owner_username": owner_username,
                        "owner_full_name": owner_full_name,
                        "business_category_name": business_cn,
                        "category_name": category_cn,
                        "profile_type": profile_type,
                        "location_lat": location_lat,
                        "location_lng": location_lng,
                        "location_name": location_name,
                        "city": city,
                        "admin1": admin1,
                        "admin2": admin2,
                        "country_iso2": country_iso2,
                        "gender": gender,
                        "obj_img": obj_img,
                        "top_labels": top_labels,
                        "color_img": ig_img.colors,
                        "brands": brands,
                        "keywords": keywords,
                        "top_keyword": top_keyword,
                        TARGET: target_img,
                    }
                    data = {field: data[field] if field in data else None for field in IMG_DB_FIELDS}
                    data_from_images.append(data)
                except Exception:
                    print(f"Problemas con {filename}")
            ids.append(shortcode)
        return data_from_images, ids

    @staticmethod
    def ig_profile_type(business_category_name, category_name, gender, owner_full_name=None, sim_th=85):
        for category in IG_BUSINESS_CATEGORY:
            if business_category_name in IG_BUSINESS_CATEGORY[category]:
                return category
        for category in IG_CATEGORY:
            if category_name in IG_CATEGORY[category]:
                return category
        if owner_full_name not in [None, "null", "None"]:
            clean_text = re.sub(r"[/-]", " ", NlpUtils.norm_text(owner_full_name).lower())
            for word in clean_text.split():
                for term in BUSINESS_NAME_WORDS:
                    if fuzz.ratio(word, term) >= sim_th:
                        return "business"
        if gender in ["F", "M"]:
            return "person"
        else:
            return "business"

    @staticmethod
    def location_from_text(row, loc_fields):
        locs, loc_temp, cities, countries = [], [], [], []
        for col_name, ec in loc_fields.items():
            lang = row["lang"] if "lang" in row and row["lang"] in LANGUAGES else None
            loc_temp += Location().get_locations(row[col_name], ec, lang)
        for loc in loc_temp:
            cty, cntry = loc["city"], loc["country"]
            if cty not in ["", None, np.nan]:
                cities.append(cty)
                if loc not in locs:
                    locs.append(loc)
            if cntry not in ["", None, np.nan]:
                countries.append(cntry)
        top_city = mode(cities) if cities else None
        top_country = mode(countries) if countries else None
        return locs, top_city, top_country

    @staticmethod
    def terms_detection(text, terms):
        doc = NlpUtils.norm_text(str(text).lower())
        return [t for t in terms if t.lower() in doc]


class IngestData:
    @staticmethod
    def instagram_terms_to_S3(terms=IG_TERMS):
        ig_instance = Instagram(token=IG_TOKEN)
        for term in terms:
            try:
                ig_instance.upload_hashtag_media_to_s3(
                    query=term,
                    bucket_name=BUCKET_NAME,
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
                )
                print(f"Busqueda de término '{term}' finalizada. Datos cargados en S3 {BUCKET_NAME}.")
            except Exception:
                print(f"Problemas con término '{term}'")
                traceback.print_exc()

    @staticmethod
    def instagram_locations_to_S3(locations=LOCATIONS):
        ig_instance = Instagram(token=IG_TOKEN)
        for location_id in locations:
            try:
                ig_instance.upload_located_posts_media_to_s3(
                    location_id=location_id,
                    days_limit=DAYS_LIMIT,
                    bucket_name=BUCKET_NAME,
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                )
                print(f"Busqueda para location_id {location_id} finalizada. Datos cargados en S3 {BUCKET_NAME}.")
            except Exception:
                print(f"Problemas con location_id {location_id}")
                traceback.print_exc()

    @staticmethod
    def twitter(terms=TW_TERMS, max_tweets=MAX_TWEETS_PER_TERM, update_db=True):
        tw_instance = Twitter(
            twitter_consumer_key=TW_CONN["consumer_key"],
            twitter_consumer_secret=TW_CONN["consumer_secret"],
            twitter_key=TW_CONN["access_key"],
            twitter_secret=TW_CONN["access_secret"],
        )
        tw_data = tw_instance.fetch_terms_tweets(terms=terms, max_tweets_per_term=max_tweets)
        if update_db:
            tw_df = pd.DataFrame(tw_data[0])
            _ = MySQLtools(table="tweets").update_table(input_df=tw_df, keys=KEYS["tweets"], batch=300)
        return tw_data


class StatsETL:
    def build_tables(self, source, date_col=DATE_COL, date_range=None):
        """
        :Description: pre-calcular tablas de estadísticas
        :param source: red social -'twitter' o 'instagram'- (:type: string)
        :param date_col: nombre de la columna que contiene las fechas (:type: str)
        :param date_range: rango de fechas seleccionado (:type: list)
        :return:
        """
        if not date_range:
            date_range = [(date.today() - timedelta(days=1)).strftime("%Y-%m-%d")] * 2
        if source == "instagram":
            query = f"SELECT `{DATE_COL}`, country_iso2, admin1, clean_text FROM images WHERE `{DATE_COL}` " \
                    f"BETWEEN '{date_range[0]}' and '{date_range[1]}' and {TARGET} = 1"
        elif source == "twitter":
            query = f"SELECT `{DATE_COL}`, country_iso2, admin1, clean_text FROM tweets WHERE `{DATE_COL}` " \
                    f"BETWEEN '{date_range[0]}' and '{date_range[1]}' and {TARGET} = 1"
        else:
            print("Redes sociales soportadas: 'twitter' o 'instagram'")
            return
        df = MySQLtools().read_mysql_df(query)
        if df.shape[0] == 0:
            return
        words_df = self.words(
            df,
            source=source,
            dim_cols=[date_col, "country_iso2", "admin1"],
            text_col="clean_text",
            date_col=date_col,
            date_range=date_range,
        )  # Palabras
        # Actualizar tablas
        MySQLtools(table="words").update_table(words_df, KEYS["words"])

    @staticmethod
    def words(df, source, dim_cols, text_col, date_col=DATE_COL, date_range=None):
        """
        :Description: pre-calcular tabla - palabras
        :param source: red social -'twitter' o 'instagram'- (:type: string)
        :param df: tabla de entrada (:type: pandas.DataFrame)
        :param dim_cols: columnas para las cuales se agruparán las métricas (:type: list)
        :param text_col: columna que contiene el texto a procesar (:type: str)
        :param date_col: nombre de la columna que contiene las fechas (:type: str)
        :param date_range: rango de fechas seleccionado (:type: list)
        :return: tabla pre-calculada (:type: dict)
        """
        df_temp = CalcUtils.filter_date_range(df, date_col, date_range)
        df_temp = df_temp[~df_temp[text_col].isin([np.nan, None, "", " "])]
        table = []
        if len(df_temp):
            for index, row in df_temp.iterrows():
                dict_temp = {k: row[k] for k in dim_cols}
                for word in row[text_col].split():
                    if word[0] == "@":
                        w_type = "mencion"
                    elif word[0] == "#":
                        w_type = "hashtag"
                    else:
                        w_type = "palabra"
                    table.append(
                        {
                            **dict_temp,
                            "source": source,
                            "word": word,
                            "freq": 1,
                            "w_type": w_type,
                        }
                    )
            table = pd.DataFrame(table)
            table = pd.DataFrame(
                CalcUtils().groupby_df(
                    table, dim_cols + ["word", "w_type", "source"], {"freq": "sum"}
                )
            )
        else:
            table = pd.DataFrame(table)
        return table


class Responding:
    """
    :Date: 2022-11-22
    :Version: 0.2
    :Author: Joan Felipe Mendoza - Whale & Jaguar Consultants S.A.S.
    :Description: ENVIAR MENSAJES A USUARIOS
    """
    def __init__(self):
        # Inicializar instancia
        self.instance = Twitter(
                twitter_consumer_key=TW_CONN["consumer_key"],
                twitter_consumer_secret=TW_CONN["consumer_secret"],
                twitter_key=TW_CONN["access_key"],
                twitter_secret=TW_CONN["access_secret"],
            )

    def twitter_dm(self, contacts):
        data = pd.DataFrame()
        if contacts:
            # Enviar mensajes por DM
            for contact in contacts:
                if contact["screen_name"] not in BRANDS["twitter"]:
                    if contact["user_name"]:
                        name = NlpUtils.norm_text(contact["user_name"], preserve_es_char=True)
                        words = name.split()
                        if words and len(words[0]) > 2:
                            greeting = f"¡{random.choice(GREETINGS)} {words[0]}!"
                        else:
                            greeting = f"¡{random.choice(GREETINGS)}!"
                    else:
                        greeting = f"¡{random.choice(GREETINGS)}!"
                    text = f"{greeting} {random.choice(TEMPLATES_DM)}"
                    sent = self.instance.send_direct_message(text=text, twitter_id=str(contact["twitter_id"]))
                    data.append(
                        {**contact,
                         "id": str(uuid.uuid4()),
                         "datestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                         "message": text,
                         "sent": sent,
                         }
                    )
        return data

    def twitter_response(self, tweets_info):
        data = pd.DataFrame()
        if tweets_info:
            # Responder tweets
            for tweet in tweets_info:
                if tweet["screen_name"] not in BRANDS["twitter"]:
                    text = f"Mensaje de prueba"
                    status_id = tweet["tweet_id"]
                    user_name = f'@{tweet["screen_name"]}'
                    sent = self.instance.write_comment(status=text, in_reply_status_id=status_id, user_name=user_name)
                    data.append(
                        {**tweet,
                         "id": str(uuid.uuid4()),
                         "datestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                         "message": text,
                         "sent": sent,
                         }
                    )
            data = pd.DataFrame(data)
        return data

    def twitter(self, tweets_info, dm=True, response=RESPONSE_TWEETS):
        responses = pd.DataFrame()
        if tweets_info:
            data = []
            for row in tweets_info:
                if row["screen_name"] not in BRANDS["twitter"]:
                    text, dm_sent, response_sent = None, 0, 0
                    # 1. Enviar mensajes por DM
                    if dm:
                        if row["user_name"]:
                            name = NlpUtils.norm_text(row["user_name"], preserve_es_char=True)
                            words = name.split()
                            if words and len(words[0]) > 2:
                                greeting = f"¡{random.choice(GREETINGS)} {words[0]}!"
                            else:
                                greeting = f"¡{random.choice(GREETINGS)}!"
                        else:
                            greeting = f"¡{random.choice(GREETINGS)}!"
                        text = f"{greeting} {random.choice(TEMPLATES_DM)}"
                        dm_sent = self.instance.send_direct_message(text=text, twitter_id=str(row["twitter_id"]))
                    # 2. Responder tweets en caso de que no se haya enviado DM
                    if response and dm_sent == 0:
                        mssg = list(TEMPLATES_RP[TEMPLATES_RP["sttm_group"] == row["sttm_group"]]["text"])
                        if len(mssg):
                            text = random.choice(mssg)
                            response_sent = self.instance.write_comment(
                                status=text,
                                in_reply_status_id=row["tweet_id"],
                                user_name=f'@{row["screen_name"]}'
                            )
                    data.append(
                        {
                            "twitter_id": row["twitter_id"],
                            "screen_name": row["screen_name"],
                            "user_name": row["user_name"],
                            "id": str(uuid.uuid4()),
                            "datestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "message": text,
                            "sent": True if max(dm_sent, response_sent) else False,
                            "dm_sent": dm_sent,
                            "response_sent": True if response_sent else False,
                            "tweet_id": row["tweet_id"],
                        }
                    )
            responses = pd.DataFrame(data)
        return responses
