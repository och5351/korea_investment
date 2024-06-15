from ..model.communicator import *
from ..database.db import DuckDB
from ..config import *
from datetime import datetime, timedelta


class AuthModel:

    def __init__(self):
        self.db_conn = DuckDB.instance().connect(DB.DB_NAME)

    def get_user_account(self):
        _, secret_key = self.db_conn.select(f"""
                    SELECT VALUE 
                    FROM {DB.CERTIFICATION}
                    WHERE KEY = 'user_account_number'
                """)

        return secret_key[0]

    def get_app_key(self):
        _, app_key = self.db_conn.select(f"""
                    SELECT VALUE 
                    FROM {DB.CERTIFICATION}
                    WHERE KEY = 'app_key'
                """)
        return app_key[0]

    def get_secret_key(self):
        _, secret_key = self.db_conn.select(f"""
                    SELECT VALUE 
                    FROM {DB.CERTIFICATION}
                    WHERE KEY = 'secret_key'
                """)

        return secret_key[0]

    def get_approval_key(self):
        _, approval_key = self.db_conn.select(f"""
                            SELECT VALUE 
                            FROM {DB.CERTIFICATION}
                            WHERE KEY = 'approval_key'
                        """)

        return approval_key[0]

    def update_approval_key(self):
        approval_key = AuthComm() \
            .get_key(
            url=COMMUNICATION_CONF.OAUTH_URL,
            app_key=self.get_app_key(),
            secret_key=self.get_secret_key()
        )['approval_key']

        self.db_conn.execute(f"""
                    INSERT INTO {DB.CERTIFICATION}
                    VALUES('approval_key', '{approval_key}', '{(datetime.today()).strftime('%Y%m%d%H%M%S%f')[:-3]}')
                    ON CONFLICT
                    DO UPDATE SET
                    value = '{approval_key}',
                    change_dttm = '{(datetime.today()).strftime('%Y%m%d%H%M%S%f')[:-3]}'
                """)

    def get_token(self):
        _, token_expired = self.db_conn.select(f"""
                            SELECT VALUE 
                            FROM {DB.CERTIFICATION}
                            WHERE KEY = 'access_token_token_expired'
                        """)

        if (not token_expired or
                (datetime.strptime(token_expired[0], '%Y-%m-%d %H:%M:%S') - datetime.now()) < timedelta(seconds=0.0)):

            response = AuthComm() \
                .get_token(
                url=COMMUNICATION_CONF.GEN_TOKEN_URL,
                app_key=self.get_app_key(),
                secret_key=self.get_secret_key()
            )

            self.db_conn.execute(f"""
                    INSERT INTO {DB.CERTIFICATION} 
                    VALUES('access_token', '{response['access_token']}' ,'{(datetime.today()).strftime('%Y%m%d%H%M%S%f')[:-3]}')
                    ON CONFLICT
                    DO UPDATE SET
                    value = '{response['access_token']}',
                    change_dttm = '{(datetime.today()).strftime('%Y%m%d%H%M%S%f')[:-3]}'
                """)

            self.db_conn.execute(f"""
                    INSERT INTO {DB.CERTIFICATION} 
                    VALUES('access_token_token_expired', '{response['access_token_token_expired']}' ,'{(datetime.today()).strftime('%Y%m%d%H%M%S%f')[:-3]}')
                    ON CONFLICT
                    DO UPDATE SET
                    value = '{response['access_token_token_expired']}',
                    change_dttm = '{(datetime.today()).strftime('%Y%m%d%H%M%S%f')[:-3]}'
                """)

            self.db_conn.execute(f"""
                    INSERT INTO {DB.CERTIFICATION} 
                    VALUES('token_type', '{response['token_type']}' ,'{(datetime.today()).strftime('%Y%m%d%H%M%S%f')[:-3]}')
                    ON CONFLICT
                    DO UPDATE SET
                    value = '{response['token_type']}',
                    change_dttm = '{(datetime.today()).strftime('%Y%m%d%H%M%S%f')[:-3]}'
                """)

            self.db_conn.execute(f"""
                    INSERT INTO {DB.CERTIFICATION} 
                    VALUES('expires_in', '{response['expires_in']}' ,'{(datetime.today()).strftime('%Y%m%d%H%M%S%f')[:-3]}')
                    ON CONFLICT
                    DO UPDATE SET
                    value = '{response['expires_in']}',
                    change_dttm = '{(datetime.today()).strftime('%Y%m%d%H%M%S%f')[:-3]}'
                """)

        _, token_type = self.db_conn.select(f"""
                                            SELECT VALUE 
                                            FROM {DB.CERTIFICATION}
                                            WHERE KEY = 'token_type'
                                        """)

        _, token = self.db_conn.select(f"""
                                    SELECT VALUE 
                                    FROM {DB.CERTIFICATION}
                                    WHERE KEY = 'access_token'
                                """)

        return f"{token_type[0]} {token[0]}"
