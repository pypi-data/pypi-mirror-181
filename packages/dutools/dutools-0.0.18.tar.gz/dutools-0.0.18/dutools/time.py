# -*- coding: utf-8 -*-
# @time: 2022/4/21 16:50
# @author: Dyz
# @file: time.py
# @software: PyCharm
import time
from hashlib import md5
from time import gmtime, strftime


def make_md5(s: str, encoding='utf-8') -> str:
    """加密"""
    return md5(s.encode(encoding)).hexdigest()


def timer(func):
    """ 计算时间装饰器 """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        time_ = strftime("%H:%M:%S", gmtime(time.time() - start_time))
        print(f'总耗时: {time_}')
        return res

    return wrapper
