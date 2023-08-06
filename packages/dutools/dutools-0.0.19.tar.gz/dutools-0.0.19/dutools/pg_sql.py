# -*- coding: utf-8 -*-
# @time: 2022/3/4 16:10
# @author: Dyz
# @file: crud.py
# @software: PyCharm


import psycopg2
import psycopg2.extras


class PostGreSql:
    def __init__(self, conf: dict, cursor_factory=psycopg2.extras.DictCursor):
        """
        DictCursor
        RealDictCursor
        conf = {'database': "db", "user": "postgres", "password": "...",
                "host": "127.0.0.1", "port": "5432"}
        """
        self.conn = psycopg2.connect(**conf, client_encoding='UTF-8')
        self.cur = self.conn.cursor(cursor_factory=cursor_factory)

    def fetchall(self, sql, dict_row=True):
        """多条数据查询 """
        self.cur.execute(sql)
        if dict_row:
            return self.to_dict(self.cur.fetchall())
        return self.cur.fetchall()

    def fetchone(self, sql, dict_row=True):
        """单条数据查询 """
        self.cur.execute(sql)
        if dict_row:
            return self.to_dict(self.cur.fetchone())
        return self.cur.fetchone()

    def to_dict(self, res):
        """结果转dict"""
        if res:
            if isinstance(res[0], list):
                return [dict(row) for row in res]
        return dict(res)

    def fetchmany(self, sql, size=None, dict_row=True):
        """大数据据查询 """
        self.cur.execute(sql)
        if dict_row:
            return self.to_dict(self.cur.fetchone())
        return self.cur.fetchmany(size)

    def commit(self, sql, data_list=None):
        '''
            cur.execute(
            "create table test (id int primary key, v1 int, v2 int)")

            execute_values(cur,
            "INSERT INTO test (id, v1, v2) VALUES %s",
            [(1, 2, 3), (4, 5, 6), (7, 8, 9)])

            execute_values(cur,
            """UPDATE test SET v1 = data.v1 FROM (VALUES %s) AS data (id, v1)
            WHERE test.id = data.id""",
            [(1, 20), (4, 50)])

            cur.execute("select * from test order by id")
            cur.fetchall()
            [(1, 20, 3), (4, 50, 6), (7, 8, 9)])
        '''
        if data_list:
            psycopg2.extras.execute_values(self.cur, sql, data_list)
        else:
            self.cur.execute(sql)
        return self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()



class PgSql:
    def __init__(self, conf: dict, cursor_factory=psycopg2.extras.DictCursor):
        self.cursor_factory = cursor_factory
        self.conn = psycopg2.connect(**conf)
        self.cur = self.conn.cursor(cursor_factory=self.cursor_factory)

    def __enter__(self):
        self.cur = self.conn.cursor(cursor_factory=self.cursor_factory)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cur.close()

    def fetchall(self, sql, dict_row=True):
        """多条数据查询 """
        self.cur.execute(sql)
        if dict_row:
            return self.to_dict(self.cur.fetchall())
        return self.cur.fetchall()

    def fetchone(self, sql, dict_row=True):
        """单条数据查询 """
        self.cur.execute(sql)
        if dict_row:
            return self.to_dict(self.cur.fetchone())
        return self.cur.fetchone()

    def to_dict(self, res):
        """结果转dict"""
        if res:
            if isinstance(res[0], list):
                return [dict(row) for row in res]
        return dict(res)

    def fetchmany(self, sql, size=None, dict_row=True):
        """大数据据查询 """
        self.cur.execute(sql)
        if dict_row:
            return self.to_dict(self.cur.fetchone())
        return self.cur.fetchmany(size)

    def commit(self, sql, data_list=None):
        '''
            cur.execute(
            "create table test (id int primary key, v1 int, v2 int)")

            execute_values(cur,
            "INSERT INTO test (id, v1, v2) VALUES %s",
            [(1, 2, 3), (4, 5, 6), (7, 8, 9)])

            execute_values(cur,
            """UPDATE test SET v1 = data.v1 FROM (VALUES %s) AS data (id, v1)
            WHERE test.id = data.id""",
            [(1, 20), (4, 50)])

            cur.execute("select * from test order by id")
            cur.fetchall()
            [(1, 20, 3), (4, 50, 6), (7, 8, 9)])
        '''
        if data_list:
            psycopg2.extras.execute_values(self.cur, sql, data_list)
        else:
            self.cur.execute(sql)
        return self.conn.commit()


if __name__ == '__main__':
    conf = {'database': "db", "user": "postgres", "password": "test", "host": "127.0.0.1",
            "port": "5432"}
    conn = PostGreSql(conf)
    sql = f'''SELECT DISTINCT * FROM "public"."test"  ORDER BY "id" LIMIT 20'''
    data = conn.fetchone(sql)
    for i in data:
        print(i)
