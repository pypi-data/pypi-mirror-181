import math
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import pymysql
from tqdm import tqdm
from classes.InsteadOfPyMySql.cuPymysql.utils import Column, DataType, Logger

@dataclass
class DatabaseManager:
    host: str
    user: str
    db: str
    password: str
    port: int
    charset: str = "utf8mb4"
    cursorclass: pymysql.cursors.Cursor = pymysql.cursors.DictCursor
    logger: Optional[Logger] = None
    db_info: Optional[Dict[str, Any]] = None

    def get_conn(self):
        if self.db_info is None:
            conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.db,
                port=self.port,
                charset=self.charset,
                cursorclass=self.cursorclass,
            )
        else:
            conn = pymysql.connect(**self.db_info)

        return conn

    def create_table(self, table: str, columns: List[Column]):
        with self.get_conn() as conn:
            with conn.cursor() as cursor:
                delete_table = f"DROP TABLE IF EXISTS {table}"
                cursor.execute(delete_table)
                conn.commit()

                sql = f"CREATE TABLE {table} ("
                for col in columns:
                    sql += f"{col.name} {col.data_type}"
                    if col.null:
                        sql += f" {DataType.NULL}"
                    else:
                        sql += f" {DataType.NOT_NULL}"
                    if col.auto_increment:
                        sql += " AUTO_INCREMENT"
                    if col.primary_key:
                        sql += " PRIMARY KEY"
                    if col.unique:
                        sql += " UNIQUE"
                    # if col.default:
                    #     sql += f" DEFAULT {col.default}"

                    sql += ","
                sql = sql[:-1] + ")"
                print(sql)
                cursor.execute(sql)
                conn.commit()

    def drop_table(self, table: str):
        with self.get_conn() as conn:
            with conn.cursor() as cursor:
                sql = f"DROP TABLE {table}"
                cursor.execute(sql)
                conn.commit()

    def insert(self, data_list: list, database, table_info, batch_size: int = 10000):
        table_name = table_info["table_name"]
        table_scheme = table_info["scheme"]
        values_format = ["%s" for i in range(len(table_scheme))]
        scheme_format = tuple(table_scheme)
        values_format = tuple(values_format)
        conn = self.get_conn()
        cursor = conn.cursor()

        try:
            # Belows are temporal solutions until we solve the error.
            # We just insert one row at a time.
            """
            for i, each in enumerate(tqdm(data_list, desc=table_name)):
                create_idx = -2
                each = tuple(each) + tuple(each[:create_idx] + each[create_idx+1:])
                update_list = [f'{scheme}={value}' for scheme, value in zip(scheme_format, values_format) if scheme != 'create_date']
                sql = "INSERT INTO RAW.{}".format(table_name) + \
                    "({})".format(",\n ".join(scheme_format)) + \
                    " VALUES({})".format(",\n".join(values_format)) + \
                    " ON DUPLICATE KEY UPDATE " + \
                    "{}".format(",".join(update_list))
                
                #import pdb; pdb.set_trace()

                cursor.execute(sql, each)
                conn.commit()
            """

            # Here is an error while conducting combined process of
            # 'INSERT INTO DUPLICATE KEY UPDATE' with cursor.executemany()
            # It isn't solved yet.

            # data_list = [tuple(each) for _, each in enumerate(data_list)]

            # Change REPLACE Query into INSERT-DUPLICATE Query.
            create_idx = -2
            data_list = [
                tuple(each) + tuple(each[:create_idx] + each[create_idx + 1 :])
                for _, each in enumerate(data_list)
            ]
            # ----------------------------------------------- #

            iteration = math.ceil(len(data_list) / batch_size)
            batch_list = [
                data_list[i * batch_size : (i + 1) * batch_size]
                if len(data_list) > (i + 1) * batch_size
                else data_list[i * batch_size :]
                for i in range(iteration)
            ]

            for i, each in enumerate(tqdm(batch_list, desc=table_name)):
                # OLD FORM
                # sql = 'REPLACE INTO RAW.{}'.format(table_name) + \
                #        '({})'.format(",\n ".join(scheme_format)) + \
                #        ' VALUES({})'.format(",\n".join(values_format))

                # Change REPLACE Query into INSERT-DUPLICATE Query.
                # There is a MySQL Bug...
                # https://stackoverflow.com/questions/12825232/python-execute-many-with-on-duplicate-key-update

                update_list = [
                    f"{scheme}={value}"
                    for scheme, value in zip(scheme_format, values_format)
                    if scheme != "create_date"
                ]
                sql = (
                    "INSERT INTO {}".format(database)
                    + ".{}".format(table_name)
                    + "({})".format(",\n ".join(scheme_format))
                    + " VALUES({})".format(",\n".join(values_format))
                    + " ON DUPLICATE KEY UPDATE "
                    + "{}".format(",".join(update_list))
                )

                cursor.executemany(sql, each)
                conn.commit()

        except Exception as e:
            self.logger.error(each)
            self.logger.error(f"Error occurred in {table_name} : {e}")
        finally:
            conn.close()

    def select(self, table: str, at: Optional[int], columns: List[str], where: str = ""):
        with self.get_conn() as conn:
            with conn.cursor() as cursor:
                sql = f"SELECT {', '.join(columns)} FROM {table}"
                if where:
                    sql += f" WHERE {where}"
                if at:
                    sql += f" LIMIT {at}"
                cursor.execute(sql)
                return cursor.fetchall()

    def select_all(self, table: str, columns: List[str]):
        with self.get_conn() as conn:
            with conn.cursor() as cursor:
                sql = f"SELECT {', '.join(columns)} FROM {table}"
                cursor.execute(sql)
                return cursor.fetchall()

    def row(self, at: int, table: str):
        with self.get_conn() as conn:
            with conn.cursor() as cursor:
                sql = f"SELECT * FROM {table} LIMIT 1 OFFSET {at}"
                cursor.execute(sql)
                return cursor.fetchone()