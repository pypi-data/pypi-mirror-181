# -*- coding: utf-8 -*-
# @time: 2022/12/5 9:42
# @author: Dyz
# @file: base_settings.py
# @software: PyCharm
# 配置文件
import json
import os
import platform

from dutools.exceptions import ConfigurationError


def get_env() -> bool:
    """以 IP 判断当前运行环境"""
    system = platform.system()
    if system == 'Linux':
        # 生产环境
        return True
    return False


class BaseSettings:
    """
    配置 基类
        判断环境
        覆盖 print 颜色
        yml配置文件
        conf.yml

          test:
            es:
                index: cards
                host: 127.0.0.1
                port: 9200
                mapping_file: cards.json
            mysql:
                ...
          env:
            es:
                index: cards
                host: 127.0.0.1
                port: 9200
                mapping_file: cards.json
    """

    def __init__(self, config_file, base_dir):
        _, extension = os.path.splitext(config_file)
        if extension in (".yml", ".yaml"):
            import yaml
            with open(os.path.join(base_dir, config_file), "r", encoding='utf-8') as f:
                config = yaml.safe_load(f)
        else:
            raise ConfigurationError('请使用 .yml 或 .yaml 格式!')

        if get_env():
            self.config = config['env']
            self.color = "\033[0;32m{}\033[0m"
            print(self.color.format('生产环境'))
        else:
            self.config = config['test']
            self.color = "\033[0;34m{}\033[0m"
            print(self.color.format('开发环境'))

    def print(self, string):
        print(self.color.format(string))


class EsSettings(BaseSettings):
    """yml配置文件
        conf.yml

          test:
              es:
                index: bios
                hosts:
                  - http://10.168.2.51:9200
                mapping_file: bios.json
              mysql:
                host: 10.168.2.160
                port: 3306
                user: biosmanage
                password: eef45A%438eb
                database: bios2022v2
                charset: utf8mb4
              pgsql:
                host: '10.168.2.160'
                port: 5432
                user: 'postgres'
                pwd: 'Xd2pgsqlgI'

            env:
              es:
                index: bios
                hosts:
                  - http://10.168.2.51:9200
                mapping_file: bios.json
              mysql:
                host: 10.168.2.160
                port: 3306
                user: biosmanage
                password: eef45A%438eb
                database: bios2022v2
                charset: utf8mb4
    """

    def __init__(self, config_file, base_dir):
        super().__init__(config_file, base_dir)

        from elasticsearch import Elasticsearch

        self.es: Elasticsearch = Elasticsearch(hosts=self.config['es']['hosts'])
        self.index: str = self.config['es']['index']
        es_index_settings = None
        if self.config['es'].get('mapping_file'):
            with open(os.path.join(base_dir, self.config['es'].get('mapping_file')), "r") as f:
                es_index_settings = json.load(f)
        self.es_ip = self.config['es']['hosts']
        self.index_conf: dict = es_index_settings

    def cat(self, sta=False):
        self.print(self.config['es'])
        if sta:
            self.print(self.index_conf)

    def _create_index(self):
        """创建索引"""
        resp = self.es.indices.create(index=self.index, body=self.index_conf)
        self.print(resp)

    def _delete_index(self):
        """删除索引"""
        s = input(f'正在删除索引, 地址: {self.es_ip}索引名: {self.index}  是否执行 (y/n):')
        if s.lower() == 'y':
            resp = self.es.indices.delete(index=self.index)
            self.print(resp)

    def _clear(self):
        """清空当前索引数据"""
        s = input(f'正在清空数据, 地址: {self.es_ip}索引名: {self.index}  是否执行 (y/n):')
        if s.lower() == 'y':
            body = {'query': {'match_all': {}}}
            resp = self.es.delete_by_query(index=self.index, body=body)
            self.print(resp)


if __name__ == '__main__':
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    settings = EsSettings('a.yml', BASE_DIR)
    print(settings.config)
