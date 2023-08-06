import math
import re

class LzNumber(object):

    # 十进制 转 十六进制
    @staticmethod
    def ten_to_hex(num: int) -> str: ...

    # 十进制 转 八进制
    @staticmethod
    def ten_to_oct(num: int) -> str: ...

    # 十进制 转 二进制
    @staticmethod
    def ten_to_bin(num: int) -> str: ...

    # 二进制 转 十进制
    @staticmethod
    def bin_to_ten(bin_str: str) -> int: ...

    # 向上取整
    @staticmethod
    def ceil(num: float) -> int: ...

    # 向下取整
    @staticmethod
    def floor(num: float) -> int: ...

    # 计算 n 次方, n=1/2表示数字的二次根号
    @staticmethod
    def pow(num: float, n: float) -> float: ...

    # 四舍五入, 保留n位小数
    @staticmethod
    def round(num: float, n: int) -> float: ...

    # 自定义舍入的值, 当小数大于等于level_num值时进行进位
    @staticmethod
    def round_n(num: float, n: int, level_num: int) -> float: ...

    # 使用千分位表示法处理
    @staticmethod
    def show_thousands(num: float) -> str: ...

    @staticmethod
    def is_int(num_str: str) -> bool: ...

    @staticmethod
    def is_float_or_double(num_str: str) -> bool: ...

    @staticmethod
    def is_number(num_str: str) -> bool: ...

    @staticmethod
    def convert_to_int(num_str: str) -> int: ...

    @staticmethod
    def convert_to_float_or_double(num_str: str) -> float: ...


class LzNumberImp(LzNumber):

    @staticmethod
    # 十进制 转 十六进制
    def ten_to_hex(num: int) -> str:
        return hex(num).lstrip("0x")

    @staticmethod
    # 十进制 转 八进制
    def ten_to_oct(num: int) -> str:
        return oct(num).lstrip("0o")

    @staticmethod
    # 十进制 转 二进制
    def ten_to_bin(num: int) -> str:
        return bin(num).lstrip("0b")

    @staticmethod
    # 二进制 转 十进制
    def bin_to_ten(bin_str: str) -> int:
        return int(bin_str, base=2)

    @staticmethod
    # 向上取整
    def ceil(num: float) -> int:
        return math.ceil(num)

    @staticmethod
    # 向下取整
    def floor(num: float) -> int:
        return math.floor(num)

    @staticmethod
    # 计算 n 次方, n=1/2表示数字的二次根号
    def pow(num: float, n: float) -> float:
        return math.pow(num, n)

    @staticmethod
    # 四舍五入, 保留n位小数
    def round(num: float, n: int) -> float:
        return round(num, n)

    @staticmethod
    # 自定义舍入的值, 当小数大于等于level_num值时进行进位
    def round_n(num: float, n: int, level_num: int) -> float:
        integer, decimal = str(num).split(".", 1)
        carry = False
        if int(decimal[n]) >= level_num:
            carry = True

        r_num = float(integer + "." + decimal[:n])
        carry_num = (1 / math.pow(10, n)) if carry is True else 0
        r_num = r_num + carry_num
        return r_num

    @staticmethod
    # 使用千分位表示法处理
    def show_thousands(num: float) -> str:
        return "{:,}".format(num)

    @staticmethod
    def is_int(num_str: str) -> bool:
        return True if re.compile(r'^\d+$').search(num_str) is not None else False

    @staticmethod
    def is_float_or_double(num_str: str) -> bool:
        return True if re.compile(r'^\d+\.\d+$').search(num_str) is not None else False

    @staticmethod
    def is_number(num_str: str) -> bool:
        return LzNumberImp.is_int(num_str) or LzNumberImp.is_float_or_double(num_str)

    @staticmethod
    def convert_to_int(num_str: str) -> int:
        return int(num_str)

    @staticmethod
    def convert_to_float_or_double(num_str: str) -> float:
        return float(num_str)



# print(LzNumberImp.is_float_or_double('3'))