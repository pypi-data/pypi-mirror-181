# -*- coding: utf-8 -*-
# @time: 2022/10/12 15:33
# @author: Dyz
# @file: pyneo4j.py
# @software: PyCharm
# pyneo4j 基于 py2neo
import string

from py2neo import Relationship, Graph, Path, Subgraph, Node


class Deque:
    """循环链表"""

    def __init__(self, data):
        self.index = 0
        self.data = data

    def get(self):
        if self.index == len(self.data):
            self.index = 0
        res = self.data[self.index]
        self.index += 1
        return res


QA = Deque([_ for _ in string.ascii_lowercase])
QN = Deque([_ for _ in string.digits])


def attr_to_str(data: dict) -> str:
    if not data:
        return ''
    attr = ''
    for k, v in data.items():
        if attr:
            attr += ', '
        if isinstance(v, str):
            v_str = f'"{v}"'
        else:
            v_str = f'{v}'
        attr += f'`{k}`: {v_str}'
    if attr:
        attr = '{' + attr + '}'
    return attr


def counting(cls):
    class MetaClass(getattr(cls, '__class__', type)):
        __var = 'n'

        def __new__(meta, name, bases, attrs):
            old_init = attrs.get('__init__')

            def __init__(*args, **kwargs):
                cls.__var = f'{QA.get()}{QN.get()}'
                if old_init:
                    return old_init(*args, **kwargs)

            @classmethod
            def get_var(cls):
                return MetaClass.__var

            new_attrs = dict(attrs)
            new_attrs.update({'__init__': __init__, 'var': get_var})
            return super(MetaClass, meta).__new__(meta, name, bases, new_attrs)

    return MetaClass(cls.__name__, cls.__bases__, cls.__dict__)


@counting
class Node:
    """节点类"""

    def __init__(self, labels: str = None, **attr):
        self.labels: str = labels
        self.attr: dict = attr or {}

    def get_var(cls):
        return cls.get_var()

    def sql(self):
        term = ''
        if self.labels:
            term += f' {self.labels}'
        attr = attr_to_str(self.attr)
        # term = f'({Node.__var}: {term.strip()} {attr})'
        print(self.__dict__)
        return term

    def __str__(self):
        return self.sql()


class Rel:
    """关系类"""

    def __init__(self, r_type: str, start: Node = None, end: Node = None, **attr):
        self.r_type: str = r_type
        self.var: str = 'r'
        self.start_node: Node = start or '(n)'
        self.end_node: Node = end or '(m)'
        self.attr: dict = attr or {}
        attr = attr_to_str(self.attr)
        s_var = self.start_node.var if isinstance(self.start_node, Node) else 'n'
        e_var = self.end_node.var if isinstance(self.end_node, Node) else 'm'

        self.term = f'[{self.var}:`{self.r_type}` {attr}]'
        self.r_rel = f'({self.start_node.var})-{self.term}->({s_var})'
        self.l_rel = f'({self.start_node.var})<-{self.term}-({e_var})'
        self.var_list = [s_var, e_var, self.var]

    def sql(self):
        term = f'{self.start_node}-{self.term}->{self.end_node}'
        return term

    def __str__(self):
        return self.sql()


class Cypher:
    var_list = list(range(0 - 9))

    def __init__(self, r_type=None, *nodes: [Node, Rel]) -> None:
        self.node = [str(row) for row in nodes]
        self.var_list = [row.var for row in nodes]
        var_str = ', '.join(self.var_list)
        print(self.node)
        print(self.var_list)
        # if r_type:
        #     term = f'{", ".join(self.node)}'.strip().strip(',') + f' RETURN {var_str}'
        #
        # self.sql = term

    # def __str__(self):
    #     return self.sql


class PyNeo:
    def __init__(self, url, auth: tuple):
        self.conn: Graph = Graph(url, auth=auth)
        ...

    def run(self, cypher: Cypher):
        self.conn.run(cypher)

    def match(self, *nodes: Node):
        return self._query(*nodes, n_type='match')

    def _query(self, *nodes: Node, n_type='match'):
        node = [str(row) for row in nodes]
        var_list = [row.var for row in nodes]
        var_str = ', '.join(var_list)
        if n_type == 'match':
            term = f'MATCH {", ".join(node)}'.strip().strip(',') + f' RETURN {var_str}'
        else:
            term = f'MATCH {"MATCH ".join(node)}'.strip() + f' RETURN {var_str}'

        print(term)
        # res = self.conn.run(term)
        # print(res)
        # return res

    def merge(self, *nodes: Node):
        return self._query(*nodes, n_type='merge')

    def where(self, pattern: str):
        """
        No1: n.name ="刘德华" and m.name="周星驰"
        No2: n.name ="刘德华" and r.name="家庭"
        """

    def create_rel(self, relation: Rel, r_sta='r'):
        """
        r_type:     关系类型
        start_node: 开始节点
        end_node:   结束节点
        r_sta:      关系指向 r 向右  l 向左  all 双向
        kwargs:     关系属性
        """
        r_sta = r_sta.lower()
        r_marge = f'MARGE {relation.r_rel}'
        l_marge = f'MARGE {relation.l_rel}'
        if r_sta == 'r':
            m = r_marge
        elif r_sta == 'l':
            m = l_marge
        else:
            m = r_marge + ' ' + l_marge
        term = f'MATCH {relation.start_node}, {relation.end_node} {m} RETURN {", ".join(relation.var_list)}'
        print(term)


a = Node('Actor', name="黄晓明")
b = Node('Actor', name="杨颖")
c = Node('Actor', name="周星驰", age=54)
r1 = Rel('前夫', a)
r2 = Rel('前夫', b, c)
conn = PyNeo("bolt://localhost:7687", auth=("neo4j", "123456"))
a = Cypher(a, b, r1, r2)
print(a)
# conn.match(s, s2, s3)
# conn.merge(s)
# conn.create_rel(r, 'l')

# class PyNeo:
#     def __init__(self):
#         self.node =

# from py2neo import Node, Relationship, Graph, Path, Subgraph
# from py2neo.matching import *
#
# from dutools import MysqlDB
# from tqdm import tqdm
#
# conf = dict(
#     host="127.0.0.1",
#     port=3306,
#     user="dyz",
#     password="metstr",
#     database="spiderdb"
# )
#
# g = Graph("bolt://localhost:7687", auth=("neo4j", "123456"))
# nodes = NodeMatcher(g)
# # rel = RelationshipMatcher(g)
# # keanu = nodes.match("sect", name="明教").all()
# # # keanu = rel.match("Person", "喜欢").all()
# # keanu = rel.match(keanu, "教主").all()
# # print(keanu)
# # n = Node('Actor', name="张无忌")
# n2 = nodes.match('Actor', name="周星驰")
# n3 = nodes.get(9231)
# print(n2.all())
# print(n3)
#
