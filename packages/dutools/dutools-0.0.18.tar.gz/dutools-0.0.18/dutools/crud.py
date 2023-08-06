# -*- coding: utf-8 -*-
# @Time    : 2021/9/1 10:05
# @Author  : DYZ
# @Software: PyCharm
"""
Learn how to upload pypi's own gadgets.
He is a common operation of mysql.
Use dictionary to return data by default
"""

import pymysql
import pymysql.cursors
from contextlib import contextmanager


class Mysql:
    """ 上下文管理MySQl """

    def __init__(self, db_dict: dict, cursorclass=pymysql.cursors.DictCursor):
        self.conn = pymysql.connect(**db_dict)
        self.cursorclass = cursorclass

    def __enter__(self):
        self.conn.ping()
        self.cur = self.cursorclass(self.conn)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cur.close()

    def fetchone(self, sql: str) -> dict:
        """ 获取单条数据 """
        self.cur.execute(sql)
        return self.cur.fetchone()

    def fetchall(self, sql: str) -> list:
        """ 获取多条数据 """
        self.cur.execute(sql)
        return self.cur.fetchall()

    def data_to_str(self, sql, data: [dict, list], up=False) -> str:
        """
        str,dict,list 转换 sql字符串
        """
        if isinstance(data, list):
            data = data[0]
        if up:
            cols = ", ".join('`{}`=%({})s'.format(k, k) for k in data.keys())  # key=Val,
            res_sql = sql % cols
            return res_sql
        else:
            cols = ", ".join('`{}`'.format(k) for k in data.keys())  # key
            val_cols = ', '.join('%({})s'.format(k) for k in data.keys())  # val
            res_sql = sql % (cols, val_cols)
            return res_sql

    def commit(self, sql: str, data=None, data_list=None, up=False):
        """ 插入操作
        :param sql: 操作的SQL语句 例如 insert into users(%s) values(%s) 或 完整sql
        :param data: 以字典方式 {'age': '123', 'name': 'fake'}
        :param data_list: 以列表方式, 多数据操作 [{'age': '123', 'name': 'fake'},{'age': 23, 'name': 'qq'}]
        :return: bool
        """
        if not data and not data_list:
            self.cur.execute(sql)  # 完整sql传入
        elif data:
            sql = self.data_to_str(sql, data, up=up)
            self.cur.execute(sql, data)  # 将字典data传入
        elif data_list:
            sql = self.data_to_str(sql, data_list)
            self.cur.executemany(sql, data_list)  # 将字典data传入
        self.conn.commit()

    def commit_all(self, data: list):
        for sql in data:
            if sql:
                self.cur.execute(sql)
        self.conn.commit()


class MysqlDB:
    """ 保持会话MySQl """

    def __init__(self, db_dict: dict, cursorclass=pymysql.cursors.DictCursor):
        self.conn = pymysql.connect(**db_dict, cursorclass=cursorclass)
        self.cur = self.conn.cursor()

    def close(self):
        self.cur.close()
        self.conn.close()

    def fetchall(self, sql: str) -> list:
        """ 查询多条结果 """
        self.conn_time()
        self.cur.execute(sql)
        return self.cur.fetchall()

    def fetchone(self, sql: str) -> dict:
        """ 查询一条条结果 """
        self.conn_time()
        self.cur.execute(sql)
        return self.cur.fetchone()


    def data_to_str(self, sql, data: [dict, list], up=False) -> str:
        """
        str,dict,list 转换 sql字符串
        """
        if isinstance(data, list):
            data = data[0]
        if up:
            cols = ", ".join('`{}`=%({})s'.format(k, k) for k in data.keys())  # key=Val,
            res_sql = sql % cols
            return res_sql
        else:
            cols = ", ".join('`{}`'.format(k) for k in data.keys())  # key
            val_cols = ', '.join('%({})s'.format(k) for k in data.keys())  # val
            res_sql = sql % (cols, val_cols)
            return res_sql

    def commit(self, sql: str, data=None, data_list=None, up=False):
        """ 插入操作
        :param sql: 操作的SQL语句 例如 insert into users(%s) values(%s)/update users set %s where id=1 或 完整sql
        :param data: 以字典方式 {'age': '123', 'name': 'fake'}
        :param data_list: 以列表方式, 多数据操作 [{'age': '123', 'name': 'fake'},{'age': 23, 'name': 'qq'}]
        :return: bool
        """
        self.conn_time()
        if not data and not data_list:
            self.cur.execute(sql)  # 完整sql传入
        elif data:
            sql = self.data_to_str(sql, data, up=up)
            self.cur.execute(sql, data)  # 将字典data传入
        elif data_list:
            sql = self.data_to_str(sql, data_list)
            self.cur.executemany(sql, data_list)  # 将字典data传入
        return self.conn.commit()

    def commit_all(self, data: list):
        self.conn_time()
        for sql in data:
            if sql:
                self.cur.execute(sql)
        return self.conn.commit()

    def conn_time(self):
        try:
            self.conn.ping()
        except Exception as e:
            print('数据库重连中..')
            self.conn_time()


@contextmanager
def mysql_ssd(db_dict) -> object:
    """ SSD 数据流 适用于超大数据查询"""
    conn = pymysql.connect(**db_dict)
    cursor = pymysql.cursors.SSDictCursor(conn)
    try:
        yield cursor
    finally:
        conn.close()
