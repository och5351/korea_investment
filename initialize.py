import duckdb
from src.config import *
from dataclasses import dataclass
from datetime import datetime


@dataclass
class USER_INFO:
    USER_ID = ""
    USER_EMAIL = ""
    USER_PHONE_NUMBER = ""
    ACCOUNT_NUM = ""
    APP_KEY = ""
    SECRET_KEY = ""


if __name__ == '__main__':

    with duckdb.connect(DB.DB_NAME) as con:

        con.sql(f"""
                CREATE TABLE IF NOT EXISTS {DB.CERTIFICATION} (
                    key varchar primary key,
                    value varchar,
                    change_dttm varchar
                )
                """)

        con.sql(f"""
                INSERT INTO {DB.CERTIFICATION}
                VALUES (
                    'user_id',
                    '{USER_INFO.USER_ID}',
                    '{(datetime.today()).strftime('%Y%m%d%H%M%S%f')[:-3]}'
                )
                ON CONFLICT
                DO UPDATE SET
                value = '{USER_INFO.USER_ID}',
                change_dttm = '{(datetime.today()).strftime('%Y%m%d%H%M%S%f')[:-3]}'
                """)

        con.sql(f"""
                INSERT INTO {DB.CERTIFICATION}
                VALUES (
                    'user_email',
                    '{USER_INFO.USER_EMAIL}',
                    '{(datetime.today()).strftime('%Y%m%d%H%M%S%f')[:-3]}'
                )
                ON CONFLICT
                DO UPDATE SET
                value = '{USER_INFO.USER_EMAIL}',
                change_dttm = '{(datetime.today()).strftime('%Y%m%d%H%M%S%f')[:-3]}'
                """)

        con.sql(f"""
                INSERT INTO {DB.CERTIFICATION}
                VALUES (
                    'user_phone_number',
                    '{USER_INFO.USER_PHONE_NUMBER}',
                    '{(datetime.today()).strftime('%Y%m%d%H%M%S%f')[:-3]}'
                )
                ON CONFLICT
                DO UPDATE SET
                value = '{USER_INFO.USER_PHONE_NUMBER}',
                change_dttm = '{(datetime.today()).strftime('%Y%m%d%H%M%S%f')[:-3]}'
                """)

        con.sql(f"""
                INSERT INTO {DB.CERTIFICATION}
                VALUES (
                    'user_account_number',
                    '{USER_INFO.ACCOUNT_NUM}',
                    '{(datetime.today()).strftime('%Y%m%d%H%M%S%f')[:-3]}'
                )
                ON CONFLICT
                DO UPDATE SET
                value = '{USER_INFO.ACCOUNT_NUM}',
                change_dttm = '{(datetime.today()).strftime('%Y%m%d%H%M%S%f')[:-3]}'
                """)

        con.sql(f"""
                INSERT INTO {DB.CERTIFICATION}
                VALUES (
                    'app_key',
                    '{USER_INFO.APP_KEY}',
                    '{(datetime.today()).strftime('%Y%m%d%H%M%S%f')[:-3]}'
                )
                ON CONFLICT
                DO UPDATE SET
                value = '{USER_INFO.APP_KEY}',
                change_dttm = '{(datetime.today()).strftime('%Y%m%d%H%M%S%f')[:-3]}'
                """)

        con.sql(f"""
                INSERT INTO {DB.CERTIFICATION}
                VALUES (
                    'secret_key',
                    '{USER_INFO.SECRET_KEY}',
                    '{(datetime.today()).strftime('%Y%m%d%H%M%S%f')[:-3]}'
                )
                ON CONFLICT
                DO UPDATE SET
                value = '{USER_INFO.SECRET_KEY}',
                change_dttm = '{(datetime.today()).strftime('%Y%m%d%H%M%S%f')[:-3]}'
                """)

