import duckdb


class SingletonInstance:
    """
    @ DB 커넥션을 하나만 뽑기 위한 Singleton
    """
    __instance = None

    @classmethod
    def __getInstance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls.__instance = cls(*args, **kargs)
        cls.instance = cls.__getInstance
        return cls.__instance


class DuckDB(SingletonInstance):
    """
    @ duckdb 모델
    """

    def __init__(self):
        self.conn: duckdb = None

    def connect(self, db_name: str):
        self.conn = duckdb.connect(db_name)

        return self

    def execute(self, query: str):
        self.conn.sql(query)

        return self

    def select(self, query: str):

        elem = None
        try:
            elem = self.conn.sql(query).fetchall()[0]
        finally:
            return self, elem

    def close(self):
        self.conn.close()
