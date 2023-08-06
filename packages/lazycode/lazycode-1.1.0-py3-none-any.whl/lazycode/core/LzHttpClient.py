import requests
from lxml import etree
import json


class LzHttpClient(object):
    __headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
    }

    __context = None
    __data = None

    __response = None

    def get_text(self, url, params: dict = None, cookies: dict = None, headers: dict = None, timeout=10,
                 encoding='utf-8'):
        headers = self.__headers if headers is None else headers

        res = requests.get(url=url, headers=headers, params=params, cookies=cookies, timeout=timeout)
        res.encoding = encoding

        self.__context = res.text
        self.__response = res
        return self

    def post_text(self, url, data: dict = None, cookies: dict = None, headers: dict = None, timeout=10,
                  encoding='utf-8'):
        res = requests.post(url=url, data=json.dumps(data, ensure_ascii=False), headers=headers, cookies=cookies,
                            timeout=timeout)
        res.encoding = encoding
        self.__context = res.text
        self.__response = res
        return self

    def convert_context_to_dict(self):
        """
        将请求到的数据通过json解析为字典
        :return:
        """
        self.__data = json.loads(self.__context)
        return self

    def convert_context_to_etree(self):
        """
        将请求到底数据转换为 xpath 的etree对象
        :return:
        """
        self.__data = etree.HTML(self.__context)
        return self

    def xpath(self, xpath_str: str):
        """
        使用xpath获取数据
        :param xpath_str:
        :return:
        """
        res = self.__data.xpath(xpath_str)
        return res

    def xpath_reverse_to_string(self, obj):
        """
        将xpath对象转换为字符串
        :param obj:
        :return:
        """
        return etree.tostring(obj, pretty_print=True).decode('utf-8')

    def __str__(self):
        return str(self.__data)

# lz = LzHttpClient()
#
# div = lz.get_text('http://www.baidu.com').convert_context_to_etree().xpath('//div')
# print(lz.xpath_reverse_to_string(div[-1]))
