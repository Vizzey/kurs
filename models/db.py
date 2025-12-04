# models/db.py
import pymysql
from pymysql.cursors import DictCursor

class DBContextManager:
    def __init__(self, config):
        self.config = config
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = pymysql.connect(
            host=self.config['DB_HOST'],
            port=int(self.config.get('DB_PORT', 3306)),
            user=self.config['DB_USER'],
            password=self.config['DB_PASSWORD'],
            database=self.config['DB_NAME'],
            cursorclass=DictCursor,
            autocommit=True,
            charset='utf8mb4',   
            use_unicode=True,   
            init_command="SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, et, ev, tb):
        if self.cursor: self.cursor.close()
        if self.conn: self.conn.close()

    def select(self, sql, params=None):
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()
