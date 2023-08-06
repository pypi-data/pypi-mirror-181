# -*- coding: utf-8 -*-
# @time: 2022/4/14 14:32
# @author: Dyz
# @file: translator.py
# @software: PyCharm

import json
import random
import re
import asyncio

import httpx
import urllib3
from urllib.parse import quote

# from .constant import LANGUAGES, DEFAULT_SERVICE_URLS
LANGUAGES, DEFAULT_SERVICE_URLS = {}, ()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URLS_SUFFIX = [re.search('translate.google.(.*)', url.strip()).group(1) for url in DEFAULT_SERVICE_URLS]
URL_SUFFIX_DEFAULT = 'cn'


class AsyncGoogle:
    """异步谷歌翻译"""

    def __init__(self, url_suffix="cn", timeout=5, proxies=None, http2=False):
        self.proxies = proxies
        self.http2 = http2
        if url_suffix not in URLS_SUFFIX:
            self.url_suffix = URL_SUFFIX_DEFAULT
        else:
            self.url_suffix = url_suffix
        url_base = "https://translate.google.{}".format(self.url_suffix)
        self.url = url_base + "/_/TranslateWebserverUi/data/batchexecute"
        self.timeout = timeout
        self.headers = {
            "Referer": "http://translate.google.{}/".format(self.url_suffix),
            "Accept-Encoding": "gzip",
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; WOW64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/47.0.2526.106 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
        }

    def _package_rpc(self, text, lang_src='auto', lang_tgt='auto'):
        """传参"""
        GOOGLE_TTS_RPC = ["MkEWBc"]
        # parameter = [[text.strip(), lang_src, lang_tgt, True], [1]]
        parameter = [[text, lang_src, lang_tgt, True], [1]]
        escaped_parameter = json.dumps(parameter, separators=(',', ':'))
        rpc = [[[random.choice(GOOGLE_TTS_RPC), escaped_parameter, None, "generic"]]]
        espaced_rpc = json.dumps(rpc, separators=(',', ':'))
        freq_initial = "f.req={}&".format(quote(espaced_rpc))
        freq = freq_initial
        return freq

    def _package_rpc2(self, text, lang_src='auto', lang_tgt='auto'):
        """传参"""
        GOOGLE_TTS_RPC = ["MkEWBc"]
        # parameter = [[text.strip(), lang_src, lang_tgt, True], [1]]
        parameter = [[text, lang_src, lang_tgt, True], [1]]
        escaped_parameter = json.dumps(parameter, separators=(',', ':'))
        rpc = [[[random.choice(GOOGLE_TTS_RPC), escaped_parameter, None, "generic"]]]
        espaced_rpc = json.dumps(rpc, separators=(',', ':'))
        freq_initial = "f.req={}&".format(quote(espaced_rpc))
        freq = freq_initial
        return freq

    async def _requests(self, data):
        """请求"""
        async with httpx.AsyncClient(headers=self.headers, proxies=self.proxies, http2=self.http2) as sess:
            # async with self.sess as sess:
            resp = await sess.post(self.url, data=data, timeout=self.timeout)
            return resp.text

    async def _parse(self, r, pronounce):
        """解析"""
        response = json.loads(r[4:].strip())
        try:
            response = json.loads(response[0][2])
            response_ = list(response)
            response = response_[1][0]
            if len(response) == 1:
                if len(response[0]) > 5:
                    sentences = response[0][5]
                else:  ## only url
                    sentences = response[0][0]
                    if pronounce == False:
                        return sentences
                    elif pronounce == True:
                        return [sentences, None, None]
                translate_text = ""
                for sentence in sentences:
                    sentence = sentence[0]
                    # translate_text += sentence.strip() + ' '
                    translate_text += sentence + ' '
                translate_text = translate_text
                if pronounce == False:
                    return translate_text
                elif pronounce == True:
                    pronounce_src = (response_[0][0])
                    pronounce_tgt = (response_[1][0][0][1])
                    return [translate_text, pronounce_src, pronounce_tgt]
            elif len(response) == 2:
                sentences = []
                for i in response:
                    sentences.append(i[0])
                if pronounce == False:
                    return sentences
                elif pronounce == True:
                    pronounce_src = (response_[0][0])
                    pronounce_tgt = (response_[1][0][0][1])
                    return [sentences, pronounce_src, pronounce_tgt]
        except Exception as e:
            raise e
        return ''

    async def translate(self, text, lang_tgt='auto', lang_src='auto', pronounce=False):
        try:
            lang = LANGUAGES[lang_src]
        except:
            lang_src = 'auto'
        try:
            lang = LANGUAGES[lang_tgt]
        except:
            lang_src = 'auto'
        text = str(text)
        if len(text) >= 5000:
            return "警告：只能检测不到 5000 个字符"
        if len(text) == 0:
            return ""
        data = self._package_rpc(text, lang_src, lang_tgt)
        response = await self._requests(data=data)

        res = await self._parse(response, pronounce)
        return res


ag = AsyncGoogle()


async def google_transl(data, lang_tgt='zh'):
    result = await ag.translate(data, lang_tgt=lang_tgt)
    return result


if __name__ == '__main__':
    ...
    # data = [
    #     "For other COVID-19 related advisories for F&B establishments, see Safe Distancing Measures."
    #     "For information on VDS and ceasing of On-Arrival Testing at wholesale markets, see SMMs at wholesale markets.",
    #     "For information on food safety during this Covid-19 period, see COVID-19 and food safety.",
    # ]
    # google = AsyncGoogle()
    # task_ist = []
    # for i in data:
    #     task = asyncio.create_task(google.translate(i, 'zh'))
    #     task_ist.append(task)
    # res = asyncio.gather(*task_ist)
    # print(res)
