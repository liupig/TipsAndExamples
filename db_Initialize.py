import psycopg2
import pymysql
from configuration import (PG_DATABASE, PG_HOST, PG_PASSWORD, PG_PORT, PG_USER,
                           MYSQL_USER, MYSQL_PORT, MYSQL_HOST, MYSQL_DATABASE, MYSQL_PASSWORD)


class PGInitialize(object):
    def __init__(self):
        self.conn = psycopg2.connect(database=PG_DATABASE, user=PG_USER, password=PG_PASSWORD, host=PG_HOST,
                                     port=PG_PORT)
        self.cursor = self.conn.cursor()

    def select(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()


class MYSQLInitialize(object):
    def __init__(self):
        self.conn = pymysql.connect(host=MYSQL_HOST, port=int(MYSQL_PORT), user=MYSQL_USER, passwd=MYSQL_PASSWORD,
                                    db=MYSQL_DATABASE, charset='utf8')
        self.cursor = self.conn.cursor()

    def select(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def insert(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()

    def delete(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()

    def update(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()
