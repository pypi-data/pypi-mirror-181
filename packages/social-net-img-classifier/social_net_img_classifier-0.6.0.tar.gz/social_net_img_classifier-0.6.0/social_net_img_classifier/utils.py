import re
import traceback

import unicodedata

import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz
from nltk import ngrams
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import sent_tokenize
# Install instructions in https://spacy.io/usage
import es_core_news_sm
import en_core_web_sm

from social_net_img_classifier.settings import DATA_DIR, LANGUAGES, STOP_WRDS

DATE_COL = "date"
LANG_DICT = {"es": "spanish", "en": "english", "pt": "portuguese"}

COUNTRIES_DF = pd.read_csv(f"{DATA_DIR}/countries_table.csv", sep=";")
CITIES_DF = pd.read_csv(f"{DATA_DIR}/cities_table.csv", sep=";")
COUNTRY_CODES = [
    str(x) for x in COUNTRIES_DF["countrycode"] if x not in [None, np.nan, "ES"]
] + [str(x) for x in COUNTRIES_DF["countrycode_iso3"] if x not in [None, np.nan]]
COUNTRY_NAMES, DENONYMS = {}, {}
for lng in LANGUAGES:
    COUNTRY_NAMES[lng] = [
        str(x) for x in COUNTRIES_DF[f"countryname_{lng}"] if x not in [None, np.nan]
    ]
    DENONYMS[lng] = [
        str(x) for x in COUNTRIES_DF[f"denonym_{lng}"] if x not in [None, np.nan]
    ]

ES_CHAR_MAP = [
    ("ñ", "-*_n_?|"),
    ("Ñ", "-*_N_?|"),
    ("á", "-*_a_?|"),
    ("é", "-*_e_?|"),
    ("í", "-*_i_?|"),
    ("ó", "-*_o_?|"),
    ("ú", "-*_u_?|"),
    ("Á", "-*_A_?|"),
    ("É", "-*_E_?|"),
    ("Í", "-*_I_?|"),
    ("Ó", "-*_O_?|"),
    ("Ú", "-*_U_?|"),
]

SE_REX = [r'\best(?:are|oy|uve)\b', r'\bh(?:abre|e|ube)\s(?:estado|sido)\b',
          r'\byo\sest(?:aba|aria|e|uviera|uviere|uviese)\b',
          r'\byo\sh(?:abia|abria|aya|ubiera|ubiere|ubiese)\s(?:estado|sido)\b',
          r'\bfui\b', r'\bs(?:ere|oy)\b',
          r'\byo\s(?:era|sea|seria)\b', r'\byo\sf(?:uera|uere|uese)\b']

# Listas
names_df = pd.read_csv(f"{DATA_DIR}/names_gender.csv", sep=";")
M_LIST = names_df[names_df["gender"] == "M"]["name"].to_list()
F_LIST = names_df[names_df["gender"] == "F"]["name"].to_list()

ST = 90  # Umbral de similaridad (Levenshtein)


class NlpUtils:
    """
    :Date: 2022-10-28
    :Version: 0.6.1
    :Author: Joan Felipe Mendoza - Whale & Jaguar Consultants S.A.S.
    :Description: FUNCIONES AUXILIARES
    """

    @staticmethod
    def norm_text(text, preserve_es_char=False):
        """
        :Description: limpiar texto removiendo caracteres extraños, líneas vacías y espacios duplicados
        :param text: documento (:type: str)
        :param preserve_es_char: TRUE - presevar caracteres en español (:type: bool)
        :return: documento limpio (:type: str)
        """
        try:
            doc = text
            if preserve_es_char:
                for c in ES_CHAR_MAP:
                    doc = doc.replace(c[0], c[1])
                doc = unicodedata.normalize("NFKD", doc).encode("ascii", "ignore").decode("ascii")
                for c in ES_CHAR_MAP:
                    doc = doc.replace(c[1], c[0])
            else:
                doc = unicodedata.normalize("NFKD", doc).encode("ascii", "ignore").decode("ascii")
            doc = doc.replace("_", " ").replace(r"\x0c", "")
            doc = re.sub(r"\f+", "", doc)  # Remover caracter problemático
            doc = re.sub(r"(\r\n)+", r"\r\n", doc)  # Remover líneas vacías
            doc = re.sub(r"\n+", r"\n", doc)  # Remover líneas vacías
            doc = re.sub(r" +", r" ", doc)  # Remover múltiples espacios
            return doc
        except Exception:
            return text

    @staticmethod
    def remove_punctuation(text):
        """
        :Description: remover signos de puntuación de un texto
        :param text: texto a procesar
        :return: texto sin signos de puntuación
        """
        try:
            punctuation = {"/", '"', "(", ")", ".", ",", "%", ";", "?", "¿", "!", "¡", ":", "$", "&", ">", "<", "-",
                           "°", "|", "¬", "\\", "*", "+", "[", "]", "{", "}", "=", "'", "…"}
            for sign in punctuation:
                text = text.replace(sign, " ")
            return text
        except Exception:
            return None

    @staticmethod
    def get_item(values_list, mode=1):
        """
        :Description: devolver un valor de una lista de acuerdo a un modo de selección
        :param values_list: lista con valores (:type: list)
        :param mode: 1 - más frecuente; 2 - más largo (:type: int)
        :return: valor seleccionado
        """
        try:
            if mode == 2:
                output = values_list[
                    np.argmax([len(c.split(" ")) for c in values_list])
                ]
            else:  # mode == 1
                vdict = {
                    x: values_list.count(x) for x in values_list
                }  # Crear diccionario de frecuencias
                filterdict = dict()
                # Filtrar elementos con máxima frecuencia
                for (key, value) in vdict.items():
                    if value == max(vdict.values()):
                        filterdict[key] = value
                # Devolver el primer elemento con máxima frecuencia considerando el orden de aparición
                output = list(filterdict.keys())[0]
            return output
        except Exception:
            return ""

    def clean_text(self, text, lang=None):
        """
        :Description: limpiar texto
        :param text: texto a limpiar
        :param lang: idioma
        :return: texto limpio
        """
        try:
            stpwrds = list(STOP_WRDS)  # Configurar stopwords
            if lang in LANG_DICT:
                stpwrds += stopwords.words(LANG_DICT[lang])
            else:
                for lng in LANGUAGES:
                    stpwrds += stopwords.words(LANG_DICT[lng])
            output = text.lower()  # converts to lowercase
            output = (
                unicodedata.normalize("NFKD", output)
                .encode("ascii", "ignore")
                .decode("ascii")
            )
            output = re.sub("[\r\n\f]", " ", output)
            output = re.sub("rt @[A-Za-z0-9_]+: ", "", output)  # removes RTs
            output = re.sub(
                " ?(f|ht)(tp)(s?)(://)(.*)[.|/](.*)", "", output
            )  # removes URLs
            output = self.remove_punctuation(output)  # removes punctuation
            output = " ".join(
                [word for word in output.split() if word not in stpwrds]
            )  # stopwords
            output = re.sub(" +", " ", output)
            return output
        except Exception:
            return ""

    @staticmethod
    def stem_text(text, lang=None):
        """
        :param text: texto a limpiar str
        :param lang: idioma str
        :return outputtext: texto limpio str
        """
        try:
            lang = "es" if not lang else lang
            stemmer = SnowballStemmer(LANG_DICT[lang])
            stemmed = [stemmer.stem(word) for word in text.split()]
            return " ".join(stemmed)
        except Exception:
            traceback.print_exc()
            return None

    @staticmethod
    def lemma_text(text, lang=None):
        """
        :param text: texto a limpiar str
        :param lang: idioma str
        :return outputtext: texto limpio str
        """
        try:
            if lang == "en":
                nlp = en_core_web_sm.load()
            else:
                nlp = es_core_news_sm.load()
            doc = nlp(text)
            lemmas = [tok.lemma_.lower() for tok in doc]
            return " ".join(lemmas)
        except Exception:
            traceback.print_exc()
            return None

    def match_sim_ngrams(self, doc, search_terms, sim_th=85, mode=2, extra_len=1):
        """
        :Description: extraer porciones de texto de un documento que se encuentren en una lista de búsqueda
                      usando similaridad de Levenshtein y n-gramas
        :param doc: documento (:type: str)
        :param search_terms: lista de términos a buscar (:type: list)
        :param sim_th: valor de similaridad de referencia (:type: int)
        :param mode: 1 - retorna valores en "search_terms"; 2 - retorna n-gramas en "doc" (:type: int)
        :param extra_len: número de palabra "extra" que tendrán los n-gramas versus la longitud de términos
        :return matches: lista de hallazgos (:rtype: list)
        """
        try:
            matches, matches_temp = [], []
            for term in search_terms:
                term = str(term).lower()
                lng = len(term.split())
                doc_ngrams = list(
                    set(self.get_ngrams(doc, nmin=lng, nmax=lng + extra_len))
                )
                for doc_term in doc_ngrams:
                    similarity = fuzz.ratio(str(doc_term), term)
                    if similarity >= sim_th:
                        if mode == 1:
                            matches_temp.append((term, similarity))
                        else:
                            matches_temp.append((str(doc_term), similarity))
            if len(matches_temp) > 0:
                matches = list(set([x[0] for x in matches_temp]))
            return matches
        except Exception:
            return []

    @staticmethod
    def get_ngrams(doc, nmin=1, nmax=4):
        """
        :Description: obtener todos los n-gramas en un documento
        :param doc: documento (:type: str)
        :param nmin: longitud mínima del n-grama (:type: int)
        :param nmax: longitud máxima del n-grama (:type: int)
        :return output: lista de n-gramas (:rtype: list)
        """
        try:
            output = []
            for n in range(nmin, nmax + 1):
                output += [" ".join(g) for g in ngrams(doc.split(), n=n)]
            return output
        except Exception:
            return [""]


class CalcUtils:
    """
    :Date: 2021-11-03
    :Version: 0.2
    :Author: Joan Felipe Mendoza - Whale & Jaguar Consultants S.A.S.
    :Description: FUNCIONES DE SOPORTE
    """

    @staticmethod
    def filter_date_range(df, date_col=DATE_COL, date_range=None):
        """
        :Description: filtrar tabla por rango de fechas
        :param df: tabla a filtrar (:type: pandas.DataFrame)
        :param date_col: nombre de la columna que contiene las fechas (:type: str)
        :param date_range: rango de fechas seleccionado (:type: list)
        :return: tabla filtrada (:type: pandas.DataFrame)
        """
        if date_range is not None:
            output = df[df[date_col].between(date_range[0], date_range[1])]
        else:
            output = df.copy()
        return output

    @staticmethod
    def sort_limit_df(df, sort_col, n_items=None, ascending=False):
        """
        :Description: ordenar una tabla seleccionando los primeros elementos -si así se quiere-
        :param df: tabla a ordenar (:type: pandas.DataFrame)
        :param sort_col: nombre de la columna a partir de la cual se ordenará la tabla (:type: str)
        :param n_items: número de filas a seleccionar (:type: int)
        :param ascending: lógica de orden -True: de menor a mayor; False: de mayor a menor- (:type: boolean)
        :return: tabla ordenada (:type: pandas.DataFrame)
        """
        output = df.sort_values(by=sort_col, ascending=ascending)
        if n_items is None:
            return output
        else:
            return output.head(n_items)

    def groupby_df(self, df, groupby_cols, metrics_agg, date_col=DATE_COL, date_range=None):
        """
        :Description: agrupar tabla considerando columnas de agrupación y métricas a agregar
        :param df: tabla a agrupar (:type: pandas.DataFrame)
        :param groupby_cols: columnas para las cuales se agruparán las métricas (:type: list)
        :param metrics_agg: métricas a agregar {'metrica1': 'función_agregación1', ...} (:type: dict)
        :param date_col: nombre de la columna que contiene las fechas (:type: str)
        :param date_range: rango de fechas seleccionado (:type: list)
        :return: tabla agrupada (:type: pandas.DataFrame)
        """
        output = self.filter_date_range(df, date_col, date_range)
        output[groupby_cols] = output[groupby_cols].fillna(value="")
        return output.groupby(groupby_cols, as_index=False).agg(metrics_agg)


class Location:
    """
    :Date: 2022-10-27
    :Version: 0.2.1
    :Author: Joan Felipe Mendoza - Whale & Jaguar Consultants S.A.S.
    :Description: EXTRAER UBICACIÓN DENTRO DE UN TEXTO
    """

    def get_locations(self, text, explore_cities=True, lang=None):
        """
        :Description: extraer ubicaciones -ciudad y país- a partir de un texto dado.
        :param text: texto que posiblemente contiene ubicaciones
        :param explore_cities: True-explora ciudades y países; False-explora sólo países
        :param lang: idioma (:type: str)
        :return: lista de ubicaciones especificando ciudad y país (:type: list of dicts)
        """
        try:
            output = []
            if lang not in LANGUAGES:
                countries_list, denonyms_list = [], []
                for lng in LANGUAGES:
                    countries_list += COUNTRY_NAMES[lng]
                    denonyms_list += DENONYMS[lng]
                countries_list = list(set(countries_list))
                denonyms_list = list(set(denonyms_list))
            else:
                countries_list = COUNTRY_NAMES[lang]
                denonyms_list = DENONYMS[lang]
            # Identificar países
            cntr_fn = self.place_names(text, countries_list)
            cntr_fn = [self.std_country(country) for country in cntr_fn]
            cntr_cd = self.place_names(text, COUNTRY_CODES, lowercase=False)
            cntr_cd = [self.std_country(country) for country in cntr_cd]
            cntr_dn = NlpUtils().match_sim_ngrams(text, denonyms_list, mode=1, extra_len=0)
            cntr_dn = [self.std_country(country, denonym=True) for country in cntr_dn]
            countries = list(set(cntr_fn + cntr_cd + cntr_dn))
            # Identificar ciudades
            if explore_cities:
                cities = self.place_names(text, self.filter_cities(""))
                cntr = []
                ct = []
                for city in cities:
                    country_candidates = self.filter_countries(city)
                    for country in countries:
                        if country in country_candidates and country not in cntr:
                            # Agregar parejas ciudad-país identificadas
                            output.append({"city": city, "country": country})
                            cntr.append(country)
                            ct.append(city)
                            break
                    if city not in ct:
                        if len(country_candidates) == 1:
                            # Agregar parejas ciudad-país identificadas
                            output.append(
                                {"city": city, "country": self.std_country(country_candidates[0])}
                            )
                            cntr.append(country_candidates[0])
                        else:
                            # Agregar ciudades identificadas sin país
                            output.append({"city": city, "country": ""})
                        ct.append(city)
                countries = list(set(countries) - set(cntr))
            # Agregar países identificados sin ciudad
            for country in countries:
                output.append({"city": "", "country": country})
            return output
        except Exception:
            return []

    @staticmethod
    def place_names(doc, places, lowercase=True):
        """
        :Description: extraer posibles lugares geográficos
        :param doc: documento (:type: str)
        :param places: lista de lugares (:type: list)
        :param lowercase: indica si el documento se debe convertir a minúsculas
        :return final_places: posibles lugares (:type: str)
        """
        try:
            if lowercase:
                doc = NlpUtils.norm_text(doc.lower())  # Limpiar el texto
                rex_list = [r"\b" + str(c).lower() + r"\b" for c in places]
            else:
                doc = NlpUtils.norm_text(doc)  # Limpiar el texto
                rex_list = [r"\b" + str(c) + r"\b" for c in places]
            matches = []
            for rex in rex_list:
                matches += re.findall(re.compile(rex), doc)
            return list(set(matches))  # Devolver lugar
        except Exception:
            return []

    @staticmethod
    def std_country(country, mode="iso2", denonym=False):
        """
        :Description: estandarizar el nombre de un país a ISO de 3 caracteres
        :param country: nombre del país o gentilicio
        :param mode: tipo de respuesta. 'iso2', 'iso3', 'es', 'en'
        :param denonym: indica si "country" es un gentilicio
        :return: nombre estándar del país
        """
        if len(country) == 2:
            df = COUNTRIES_DF[COUNTRIES_DF["countrycode"] == country]
        elif len(country) == 3:
            df = COUNTRIES_DF[COUNTRIES_DF["countrycode_iso3"] == country]
        elif denonym:
            df = COUNTRIES_DF[COUNTRIES_DF["denonym_en"] == country]
            if df.shape[0] == 0:
                df = COUNTRIES_DF[COUNTRIES_DF["denonym_es"] == country]
        else:
            df = COUNTRIES_DF[COUNTRIES_DF["countryname_en"] == country]
            if df.shape[0] == 0:
                df = COUNTRIES_DF[COUNTRIES_DF["countryname_es"] == country]
        if df.shape[0] != 0:
            if mode == "es":
                output = list(df["countryname_out_es"].values)[0]
            elif mode == "en":
                output = list(df["countryname_out_en"].values)[0]
            elif mode == "iso3":
                output = list(df["countrycode_iso3"].values)[0]
            else:
                output = list(df["countrycode"].values)[0]
        else:
            output = ""
        return output

    @staticmethod
    def filter_cities(country_iso3):
        """
        :Description: filtrar listas de ciudades correspondientes a un país
        :param country_iso3: nombre del país en ISO3
        :return: lista de ciudades (:type: list)
        """
        if country_iso3 != "":
            df = CITIES_DF[CITIES_DF["countrycode_iso3"] == country_iso3]
            output = list(df["cityname"].values)
        else:
            output = list(set(CITIES_DF["cityname"].values))
        return output

    @staticmethod
    def filter_countries(city_name):
        """
        :Description: filtrar países donde hay una ciudad con el nombre especificado
        :param city_name: nombre de la ciudad
        :return: lista de países en ISO3 (:type: list)
        """
        if city_name != "":
            df = CITIES_DF[CITIES_DF["cityname"] == city_name]
            output = list(set(df["countrycode_iso3"].values))
        else:
            output = list(set(CITIES_DF["countrycode_iso3"].values))
        return output


class GenderByText:
    """
    :Date: 2022-10-27
    :Version: 0.2
    :Author: Joan Felipe Mendoza - Whale & Jaguar Consultants S.A.S.
    :Description: PREDECIR GÉNERO
    """
    def __init__(self, user_name, full_name=None, description=None, text=None):
        """
        :param user_name: usuario o "alias" (:type: str)
        :param full_name: nombre (:type: str)
        :param description: descripción (:type: str)
        :param text: texto adicional (:type: str)
        """
        self.screen_name = str(user_name)
        self.name = str(full_name)
        self.description = str(description)
        self.text = str(text)

    def predict(self):
        """
        :Description: predecir género
        :return: género -F o M- (:type: str)
        """
        gender = ""
        if self.name not in ["", None]:
            gender = self.gender_by_name(self.name, sim_th=85)  # Predecir género por nombre
        if gender == '':  # Predecir género buscando nombres en screen_name
            gender = self.gender_by_name(self.screen_name, sim_th=50)
        if gender == '' and self.description not in ['', None]:  # Predecir género analizando palabras en la descripción
            gender = self.gender_by_description()
        if gender == '' and self.text not in ['', None]:  # Predecir género analizando palabras en el texto de tweets
            gender = self.gender_by_text_es(self.text)
        return gender

    @staticmethod
    def gender_by_name(text, lang="spanish", sim_th=80):
        """
        :Description: predecir género buscando nombres femeninos y masculinos en un texto
        :param text: documento (:type: str)
        :param lang: idioma (:type: str)
        :param sim_th: umbral de similaridad (:type: int)
        :return: género -F o M- (:type: str)
        """
        words = [word for word in NlpUtils.remove_punctuation(text.lower()).split()
                 if len(word) > 2 and word not in stopwords.words(lang)]
        m_matches, f_matches = [], []
        for word in words:
            f_matches += [x for x in F_LIST if x in word]
            m_matches += [x for x in M_LIST if x in word]
        m_best, f_best, m_sim, f_sim = "", "", 0, 0
        for word in words:
            for x in f_matches:
                sim = fuzz.ratio(x, word)
                if sim > f_sim:
                    f_sim, f_best = sim, x
            for x in m_matches:
                sim = fuzz.ratio(x, word)
                if sim > m_sim:
                    m_sim, m_best = sim, x
        if m_sim > max(sim_th, f_sim):
            gender = "M"
        elif f_sim > max(sim_th, m_sim):
            gender = "F"
        else:
            gender = ""
        return gender

    def gender_by_description(self):
        """
        :Description: predecir género a partir del texto de descripción
        :return: género -F o M- (:type: str)
        """
        try:
            m_exp = r"\b(he|his|him|man|hombre|chico|boy|guy|pibe|chavo)\b"
            f_exp = r"\b(she|her|ella|mujer|chica|girl|chava|mina)\b"
            f_score = len(re.findall(re.compile(f_exp), self.description))
            m_score = len(re.findall(re.compile(m_exp), self.description))
            if f_score > m_score:
                gender = "F"
            elif m_score > f_score:
                gender = "M"
            else:
                gender = self.gender_by_pos_es(self.description)
            if gender == "":
                gender = self.gender_by_name(self.description)
            return gender
        except Exception:
            return ""

    def gender_by_text_es(self, text, sep=" *** "):
        """
        :Description: predecir género buscando en frases en primera persona del singular que indiquen si el interlocutor
                      usa el idioma español como parte del género femenino o masculino
        :param text: colección de documentos separados por "sep" (:type: str)
        :param sep: separador (:type: str)
        :return: género -F o M- (:type: str)
        """
        try:
            sentences, se_sentences = [], []
            for tweet in text.split(sep):
                sentences += sent_tokenize(tweet)
            for sent in sentences:
                doc = unicodedata.normalize("NFKD", sent.lower()).encode("ascii", "ignore").decode("ascii")
                for rex in SE_REX:
                    if len(re.findall(re.compile(rex), doc)) > 0:
                        se_sentences.append(doc)
            return self.gender_by_pos_es(re.sub(r'\.+', '.', '. '.join(se_sentences)))
        except Exception:
            return ""

    @staticmethod
    def gender_by_pos_es(text, pos="ADJ"):
        """
        :Description: predecir género buscando partes del texto (POS) que indiquen si el interlocutor usa el idioma
                      español como parte del género femenino o masculino
        :param text: documento (:type: str)
        :param pos: POS a analizar (:type: str)
        :return: género -F o M- (:type: str)
        """
        if not isinstance(pos, list):
            pos = [pos]
        try:
            nlp = es_core_news_sm.load()
            count_m, count_f, gender = 0, 0, ""
            for x in [token.text for token in nlp(text) if token.pos_ in pos]:
                if x[-2:] == "as" or x[-1:] == "a":
                    count_f += 1
                if x[-2:] == "os" or x[-1:] == "o":
                    count_m += 1
            if count_f > count_m:
                gender = "F"
            if count_m > count_f:
                gender = "M"
            return gender
        except Exception:
            return ""
