# -*- coding: utf-8 -*-
"""
-------------------------------------------------
@version    : v1.0
@author     : fangzheng
@contact    : fangzheng@yourtools-pet.cn
@software   : PyCharm
@filename   : hive.py
@create time: 2022/9/17 6:58 PM
@modify time: 2022/9/17 6:58 PM
@describe   : hive db helper
-------------------------------------------------
"""
from pyhive import hive
from .dbutils import DBConfig


class Hive:
    def __init__(self, db_config):
        """
        Construnctor for HiveHelper
        """
        self.__init_conn(db_config)

    def __init_conn(self, db_config):
        self.connect = hive.Connection(
            host=db_config['host'],
            port=db_config['port'],
            database=db_config['db'],
            username=db_config['username'])

    def get_conn(self):
        if self.connect:
            return self.connect
        else:
            self.__init_conn()
            return self.connect

    def exec_ddl_sql(self, sql):
        """
        Execute Hive SQL command，Return True or False
        :param sql: Hive SQL
        :return: True Or False
        """
        try:
            cursor = self.connect.cursor()
            result = cursor.execute(sql)
            if result is None:
                return True
        except Exception as e:
            print(sql)
            raise Exception("Execute Hive SQL Error:", e)
            return False
        finally:
            if cursor:
                cursor.close()
        return True

    def query(self, sql):
        """
        Execute Hive SQL command，Return the Query Result
        :param sql: Hive SQL
        :return: Query Result
        """
        query_rows = None
        try:
            cursor = self.connect.cursor()
            cursor.execute(sql)
            query_rows = cursor.fetchall()
        except Exception as e:
            print(sql)
            raise Exception("Execute Hive SQL Error:", e)
        finally:
            if cursor:
                cursor.close()
        return query_rows

    def close_conn(self):
        if self.connect:
            self.connect.close()
