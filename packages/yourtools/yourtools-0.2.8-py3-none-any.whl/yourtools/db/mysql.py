# -*- coding: utf-8 -*-
"""
-------------------------------------------------
@version    : v1.0
@author     : fangzheng
@contact    : fangzheng@yourtools-pet.cn
@software   : PyCharm
@filename   : mysql.py
@create time: 2022/9/17 6:58 PM
@modify time: 2022/9/17 6:58 PM
@describe   : 
-------------------------------------------------
"""
import pymysql
from .dbutils import DBConfig


class MySQL:
    def __init__(self, db_config):
        self._init(db_config)

    def _init(self, db_config):
        try:
            self.dbconfig = DBConfig(db_config)
            self._connect = pymysql.connect(
                host=str(self.dbconfig.host),
                port=self.dbconfig.port,
                user=str(self.dbconfig.username),
                passwd=str(self.dbconfig.password),
                db=str(self.dbconfig.db),
                charset=str(self.dbconfig.charset)
            )
            self.cursor = self._connect.cursor()
            return True
        except Exception as err:
            raise Exception("MySQL Connection error", err)
            return False

    def get_conn(self):
        if self._connect():
            return self._connect()
        else:
            self._init()
            return self._connect()

    def close_conn(self):
        if self._connect:
            self._connect.close()

    def query(self, sql, param=None):
        """
        Query data
        :param sql:
        :param param:
        :param size: Number of rows of data you want to return
        :return:
        """
        cur = self._connect.cursor(cursor=pymysql.cursors.DictCursor)
        rows = None
        try:
            cur.execute(sql, param)
            rows = cur.fetchall()
        except Exception as e:
            self._connect.rollback()
        cur.close()
        return rows

    def execute(self, sql):
        """
        exec DML：INSERT、UPDATE、DELETE
        :param sql: dml sql
        :return: Number of rows affected
        """
        try:
            cnt = self.cursor.execute(sql)
            self._connect.commit()
            if cnt > 0:
                return cnt
        except Exception as e:
            self._connect.rollback()
            return -1
