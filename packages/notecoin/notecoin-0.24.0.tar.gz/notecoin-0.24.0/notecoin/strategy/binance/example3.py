import pymysql
from notesecret import read_secret
from pymysql.cursors import DictCursor

engine_dict = {}
meta_dict = {}


class mysql_conn(object):
    def __init__(self, database=None, *args, **kwargs):
        self.database = database
        self.instance = None

    def __enter__(self):
        self.instance = pymysql.connect(
            host=read_secret(cate1='notecoin', cate2='dataset', cate3='mysql', cate4='host'),
            user=read_secret(cate1='notecoin', cate2='dataset', cate3='mysql', cate4='user'),
            password=read_secret(cate1='notecoin', cate2='dataset', cate3='mysql', cate4='password'),
            database=self.database,
            charset="utf8mb4",
            cursorclass=DictCursor)
        self._handle = self.instance.cursor()
        return self._handle

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._handle.close()
        self.instance.close()


def create_database(db_name):
    with mysql_conn() as conn:
        conn.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")


create_database("notecoin_okex")
