import re
from typing import List, Any, Optional, Match, AnyStr
from urllib.parse import quote, unquote, urlencode, urljoin

from lazycode.core.BaseType import BaseType


class LzStringFun1(object):
    def format(self, *args, **kwargs): ...

    # 填充到指定字符长度, fill_start_direction: -1:填充左边, 0:左右填充, 1:填充右边; 10 -> ***10
    def fill_to_length(self, fill_obj: object, fill_max_length: int, fill_start_direction: int = -1): ...

    # 字符串转bytes数据 Unicode编码: unicode_escape , UTF-8编码: UTF-8
    def to_bytes(self, encoding="UTF-8") -> bytes: ...

    # bytes数据转字符串
    def bytes_to_string(self, _bytes: bytes, encoding="UTF-8"): ...

    # 单个unicode字符串解码
    def single_string_unicode_decode(self, unicode_str: str) -> chr: ...

    # 字符串转数字
    def string_to_numbers(self) -> list: ...

    # 数字转字符串
    def numbers_to_string(self, numbers: list): ...

    # 字符串转 int
    def to_int(self) -> int: ...

    # 字符串转 float,double
    def to_float_double(self) -> float: ...

    # 字符串转 list
    def to_list(self) -> list: ...


class LzStringFun2(object):
    # 将普通字符串转换为url字符串
    def url_quote(self, string: str = None): ...

    # url字符串解码
    def url_unquote(self, string: str = None): ...

    # 将字典转换为url中, 参数键值对
    def url_encode(self, arg_dict: dict): ...

    # 拼接url, 域名 和 相对url路径
    def url_join(self, base: str, relative_url: str): ...


class LzStringFun3(object):
    '''
    | 修饰符（flags） | 描述                                                         |
    | :-------------- | :----------------------------------------------------------- |
    | re.I            | 使匹配对大小写不敏感                                         |
    | re.L            | 做本地化识别（locale-aware）匹配                             |
    | re.M            | 多行匹配，影响 ^ 和 $                                        |
    | re.S            | 使 . 匹配包括换行在内的所有字符                              |
    | re.U            | 根据Unicode字符集解析字符。这个标志影响 \w, \W, \b, \B.      |
    | re.X            | 该标志通过给予你更灵活的格式以便你将正则表达式写得更易于理解。 |
    '''

    def re_findall(self, reg: str, flags=re.S) -> List[Any]: ...

    def re_match(self, reg: str, flags=re.S) -> Optional[Match[AnyStr]]: ...

    def re_search(self, reg: str, flags=re.S) -> Optional[Match[AnyStr]]: ...

    def re_replace(self, reg: str, rep_str: str, times=0, flags=re.S) -> AnyStr: ...

    def re_split(self, reg: str, flags=re.S) -> List[AnyStr]: ...


class LzString(BaseType, LzStringFun1, LzStringFun2, LzStringFun3):
    pass


class LzStringImp(LzString):
    __value: str = None

    # ==================================================
    def __init__(self, base_type: str):
        self.init(base_type)

    def __str__(self) -> str:
        return self.to_string()

    def init(self, base_type: str):
        self.__value = base_type

    def to_string(self) -> str:
        return self.__value

    def base_type(self) -> str:
        return self.__value

    def copy(self):
        return LzStringImp(self.__value)

    # ==================================================
    def url_quote(self, string: str = None):
        if not string:
            string = self.__value
        self.__value = quote(string)
        return self

    def url_unquote(self, string: str = None):
        if not string:
            string = self.__value
        self.__value = unquote(string)
        return self

    def url_encode(self, arg_dict: dict):
        self.__value = urlencode(arg_dict)
        return self

    def url_join(self, base: str, relative_url: str):
        self.__value = urljoin(base=base, url=relative_url)
        return self

    # ==================================================
    def re_findall(self, reg: str, flags=re.S) -> List[Any]:
        return re.findall(pattern=reg, string=self.__value, flags=flags)

    def re_match(self, reg: str, flags=re.S) -> Optional[Match[AnyStr]]:
        return re.match(pattern=reg, string=self.__value, flags=flags)

    def re_search(self, reg: str, flags=re.S) -> Optional[Match[AnyStr]]:
        return re.search(pattern=reg, string=self.__value, flags=flags)

    def re_replace(self, reg: str, rep_str: str, times=0, flags=re.S) -> AnyStr:
        return re.sub(pattern=reg, repl=rep_str, string=self.__value, count=times, flags=flags)

    def re_split(self, reg: str, flags=re.S) -> List[AnyStr]:
        return re.split(pattern=reg, string=self.__value, flags=flags)

    # ==================================================
    def format(self, *args, **kwargs):
        if len(args) > 0 and len(kwargs) > 0:
            raise Exception("传入类型必须统一 集合类型 或者 字典类型")
        if args:
            self.__value = self.__value.format(*args)
        else:
            self.__value = self.__value.format(**kwargs)
        return self

    def fill_to_length(self, fill_str: str, fill_max_length: int, fill_start_direction: int = -1):
        """
        :param fill_str:
        :param fill_max_length:
        :param fill_start_direction: 填充的位置  -1: 填充在左边, 0: 两边都填充, 1: 填充在右边
        :return:
        """
        fill_left_num = 0
        fill_right_num = 0
        diff_num = fill_max_length - len(self.__value)
        diff_num = 0 if diff_num < 0 else diff_num
        if fill_start_direction < 0:
            fill_left_num = diff_num
        elif fill_start_direction == 0:
            fill_left_num = diff_num // 2
            fill_right_num = fill_left_num
            if fill_left_num + fill_right_num < diff_num:
                fill_left_num += 1
        else:
            fill_right_num = diff_num

        self.__value = (fill_str * fill_left_num) + self.__value + (str(fill_str) * fill_right_num)
        return self

    # ==================================================
    def to_bytes(self, encoding="UTF-8") -> bytes:
        return bytes(self.__value, encoding=encoding)

    def bytes_to_string(self, _bytes: bytes, encoding="UTF-8"):
        self.__value = str(_bytes, encoding=encoding)
        return self

    def single_string_unicode_decode(self, unicode_str: str) -> chr:
        """
        单个unicode字符串解码转字符
        :param unicode_str:
        :return:
        """
        return chr(int(unicode_str.strip(r"\\*[u|U]"), 16))

    def string_to_numbers(self) -> list:
        """
        字符集转数字编码
        :return:
        """
        numbers = [ord(s) for s in self.__value]
        return numbers

    def numbers_to_string(self, numbers: list):
        str_list = [chr(num) for num in numbers]
        self.__value = "".join(str_list)
        return self

    def to_int(self) -> int:
        return int(self.__value)

    def to_float_double(self) -> float:
        return float(self.__value)

    def to_list(self) -> list:
        return list(self.__value)
