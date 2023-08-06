import json
import re
import traceback

import numpy as np
import pandas as pd
import pymysql
from pymysql.constants import CLIENT

from social_net_img_classifier.settings import MySQL_CONN

JSON_FIELDS = ["obj_img", "top_labels", "color_img", "locations", "brands", "keywords", "media_url_https"]
NUM_TO_STR_FIELDS = ["timestamp", "date", "owner_id", "created_at", "twitter_id"]
TEXT_FIELDS = ["caption", "text", "location_name", "city", "owner_full_name", "admin1", "admin2", "user_name",
               "business_category_name", "category_name", "profile_type", "user_description", "user_location"]
TEXT_PROB = ["user_name", "user_description", "user_location"]


class MySQLtools:
    """
    :Date: 2022-10-27
    :Version: 0.6.1
    :Author: Joan Felipe Mendoza - Whale & Jaguar Consultants S.A.S.
    :Description: EJECUTAR QUERIES PARA LEER Y ACTUALIZAR TABLAS TIPO SQL EN BATCH
    """

    def __init__(self, table=None, db=MySQL_CONN["db"]):
        """
        :param table: tabla a consultar o actualizar (:type: str)
        """
        self.host = MySQL_CONN["host"]
        self.port = MySQL_CONN["port"]
        self.user = MySQL_CONN["user"]
        self.pssw = MySQL_CONN["pssw"]
        self.db = db
        self.table = table

    def read_mysql_df(self, query):
        """
        :Description: halar información desde una tabla ejecutando una query
        :param query: petición (:type: str)
        :return: resultado de la query (:type: pandas.DataFrame)
        """
        try:
            conn = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                passwd=self.pssw,
                db=self.db,
                autocommit=True,
            )
            df = pd.read_sql(query, conn)
            for field in JSON_FIELDS:
                if field in df.columns:
                    df[field] = [
                        json.loads(x) if x not in ["", None, np.nan] else None
                        for x in df[field].values
                    ]
            for field in NUM_TO_STR_FIELDS:
                if field in df.columns:
                    df[field] = df[field].astype(str)
        except Exception:
            traceback.print_exc()
            df = pd.DataFrame()
        finally:
            if "conn" in locals() or "conn" in globals():
                conn.close()
        return df

    def exe_query(self, query, param=None, multi_query=False):
        """
        :Description: ejecutar una query
        :param query: petición (:type: str)
        :param param: parámetros para la query
        :param multi_query: False - "query" contiene sólo una petición; True - "query" contiene 2 o más peticiones
        """
        success = False
        if not query:
            return
        try:
            if multi_query:
                conn = pymysql.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    passwd=self.pssw,
                    db=self.db,
                    autocommit=True,
                    client_flag=CLIENT.MULTI_STATEMENTS,
                )
            else:
                conn = pymysql.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    passwd=self.pssw,
                    db=self.db,
                    autocommit=True,
                )
            cur = conn.cursor()
            if param is None:
                cur.execute(query)
            else:
                cur.execute(query, param)
            success = True
        except Exception:
            traceback.print_exc()
        finally:
            try:
                cur.close()
            except Exception:
                traceback.print_exc()
            if "conn" in locals() or "conn" in globals():
                conn.close()
        return success

    def update_table(self, input_df, keys, batch=1000):
        """
        :Description: actualizar la información de una tabla en la base de datos
        :param input_df: información a actualizar en la tabla (:type: pandas.DataFrame)
        :param keys: campos que conforman la PRIMARY KEY de l tabla (:type: list)
        :param batch: registros a procesar por bache (:type: int)
        """
        df = input_df.where(pd.notnull(input_df), None)
        columns = [x for x in df.columns if x not in keys]
        for field in JSON_FIELDS:
            if field in df.columns:
                df[field] = [
                    json.dumps(x) if x not in ["", None, np.nan] else None
                    for x in df[field].values
                ]
        for t_field in TEXT_FIELDS:
            if t_field in df.columns:
                df[t_field] = [str(x).replace("\xa0", " ") for x in df[t_field].values]
        for t_field in TEXT_PROB:
            if t_field in df.columns:
                df[t_field] = [str(x).replace("'", "") for x in df[t_field].values]
        q_list = []  # Lista de queries
        for _, row in df.iterrows():
            key_values = tuple(row[list(keys)])
            column_values = tuple(row[list(columns)])
            query_columns = ", ".join([f"`{x}`" for x in list(keys + columns)])
            update_values = [
                self.join_as_str(columns[i], column_values[i])
                for i in range(len(columns))
            ]
            update_values = ", ".join(update_values)
            q_list.append(
                f"INSERT INTO {self.table} ({query_columns}) VALUES {key_values + column_values} ON DUPLICATE"
                f" KEY UPDATE {update_values}".replace(", None", ", NULL")
                .replace("= None", "= NULL")
                .replace(", nan", ", NULL")
                .replace("= nan", "= NULL")
                .replace(", 'nan'", ", NULL")
                .replace("= 'nan'", "= NULL")
            )
        count = 0
        success = 1
        for q in [q_list[i: i + batch] for i in range(0, len(q_list), batch)]:
            batch_success = self.exe_query("; ".join(q), multi_query=True)
            if batch_success:
                count += len(q)
                print(
                    f"Actualizando tabla: '{self.table}' | Registros agregados o modificados: {count}"
                )
            else:
                success = 0
        return success

    @staticmethod
    def join_as_str(field, value, joiner="="):
        """
        :Description: función auxiliar para unir cadenas de texto
        :param field: nombre del campo o columna (:type: str)
        :param value: valor del campo o columna  (:type: str)
        :param joiner: caracter de unión (:type: str)
        :return: cadena de texto (:type: str)
        """
        if field in TEXT_FIELDS:
            value = re.sub(r"[“”«»']", '"', value) if value else value
        if type(value) in [float, int]:
            val_str = value
        else:
            val_str = re.sub(
                r'^"',
                r"'",
                re.sub(r'"$', r"'", json.dumps(value, ensure_ascii=False)).replace(
                    '\\"', '"'
                ),
            )
        return f"`{field}` {joiner} {val_str}"


class MySQLstream:
    """
    :Date: 2022-10-20
    :Version: 0.1
    :Author: Joan Felipe Mendoza - Whale & Jaguar Consultants S.A.S.
    :Description: EJECUTAR QUERIES PARA LEER Y ACTUALIZAR TABLAS TIPO SQL EN STREAMING
    """
    @staticmethod
    def set_conn(conn=MySQL_CONN, db=MySQL_CONN["db"], multi_query=False):
        try:
            if multi_query:
                conn = pymysql.connect(
                    host=conn["host"],
                    port=conn["port"],
                    user=conn["user"],
                    passwd=conn["pssw"],
                    db=db,
                    autocommit=True,
                    client_flag=CLIENT.MULTI_STATEMENTS,
                )
            else:
                conn = pymysql.connect(
                    host=conn["host"],
                    port=conn["port"],
                    user=conn["user"],
                    passwd=conn["pssw"],
                    db=db,
                    autocommit=True,
                )
            cur = conn.cursor()
        except Exception:
            traceback.print_exc()
            conn, cur = None, None
        return conn, cur

    @staticmethod
    def close_conn(conn, cur):
        try:
            cur.close()
        except Exception:
            traceback.print_exc()
        if "conn" in locals() or "conn" in globals():
            conn.close()

    @staticmethod
    def exe_query(cur, query, param=None):
        """
        :Description: ejecutar una query
        :param query: petición (:type: str)
        :param param: parámetros para la query
        """
        if not query:
            return
        try:
            if param is None:
                cur.execute(query)
            else:
                cur.execute(query, param)
            error = None
        except Exception as e:
            traceback.print_exc()
            error = e
        return error

    def update_table_rbr(self, cur, input_data, table, keys, verbose=False):
        """
        :Description: actualizar la información de una tabla en la base de datos
        :param input_data: información a actualizar en la tabla (:type: pandas.DataFrame or list[dict])
        :param keys: campos que conforman la PRIMARY KEY de l tabla (:type: list)
        """
        input_data = pd.DataFrame(input_data)
        df = input_data.where(pd.notnull(input_data), None)
        columns = [x for x in df.columns if x not in keys]
        for field in JSON_FIELDS:
            if field in df.columns:
                df[field] = [
                    json.dumps(x) if x not in ["", None, np.nan] else None
                    for x in df[field].values
                ]
        for t_field in TEXT_FIELDS:
            if t_field in df.columns:
                df[t_field] = [str(x).replace("\xa0", " ") for x in df[t_field].values]
        failed_rows = []
        for _, row in df.iterrows():
            key_values = tuple(row[list(keys)])
            column_values = tuple(row[list(columns)])
            query_columns = ", ".join([f"`{x}`" for x in list(keys + columns)])
            update_values = [
                MySQLtools.join_as_str(columns[i], column_values[i])
                for i in range(len(columns))
            ]
            update_values = ", ".join(update_values)
            query = f"INSERT INTO {table} ({query_columns}) VALUES {key_values + column_values} ON DUPLICATE" \
                    f" KEY UPDATE {update_values}".replace(", None", ", NULL") \
                .replace("= None", "= NULL") \
                .replace(", nan", ", NULL") \
                .replace("= nan", "= NULL") \
                .replace(", 'nan'", ", NULL") \
                .replace("= 'nan'", "= NULL")
            success = self.exe_query(cur, query)
            if not success:
                failed_rows.append(row)
            else:
                if verbose:
                    print(f"Actualizando tabla: '{table}' | Registros agregados o modificados: 1")
        return pd.DataFrame(failed_rows)
