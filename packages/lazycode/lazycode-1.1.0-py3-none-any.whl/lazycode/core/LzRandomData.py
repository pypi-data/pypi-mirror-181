from lazycode.setting import random_data_file, TEMP_DIR
import json
import os
import random
import datetime
from dateutil import relativedelta
from typing import List
import pandas as pd
from abc import abstractmethod
from lazycode.core.LzMySQL import LzMySQL

all_data_dict = None
with open(random_data_file, 'r', encoding='utf-8') as f:
    all_data_dict = json.loads(f.read())


class LzRandomData(object):

    @staticmethod
    def random_university():
        return random.choice(all_data_dict["universitys"])

    @staticmethod
    def random_number(bit_num: int = 10, start_is_zero=False) -> str:
        number = list(map(str, range(0, 10)))
        number_no = list(map(str, range(1, 10)))

        num = random.choice(number_no) if start_is_zero is False else random.choice(number)
        bit_num -= 1
        if bit_num > 0:
            num += ''.join(random.choices(number, k=bit_num - 1))
        return num

    @staticmethod
    def random_name_sex() -> tuple:
        # 单姓
        firstName = all_data_dict["nameData"]["firstName"]
        # 双姓
        firstNameDouble = all_data_dict["nameData"]["firstNameDouble"]

        # 80% 的单姓
        name_first = random.choice(firstName) if random.randint(1, 100) <= 80 else random.choice(firstNameDouble)

        # 女名
        last_name_girl = all_data_dict["nameData"]["lastNameGirl"]
        last_name_girl_double = ''.join(random.choices(last_name_girl, k=2))

        last_name_boy = all_data_dict["nameData"]["lastNameBoy"]
        last_name_boy_double = ''.join(random.choices(last_name_boy, k=2))

        if random.randint(0, 1) > 0:
            # 80% 双字的名
            name_last = last_name_boy_double if random.randint(1, 100) <= 80 else random.choice(
                last_name_boy)
            sex = '男'
        else:
            name_last = last_name_girl_double if random.randint(1, 100) <= 80 else random.choice(
                last_name_girl)
            sex = '女'

        name = name_first + name_last
        return name_first, name_last, name, sex

    @staticmethod
    def random_city() -> tuple:
        cityList = all_data_dict["cityList"]
        city_level1, city_level2, city_level3 = random.choice(cityList).split("-")
        city_level1, city_level1_code = city_level1.split("_", 1)
        city_level1_code = "{:0<6}".format(city_level1_code)
        city_level2, city_level2_code = city_level2.split("_", 1)
        city_level2_code = "{:0<6}".format(city_level2_code)
        city_level3, city_level3_code = city_level3.split("_", 1)
        city_level3_code = "{:0<6}".format(city_level3_code)

        return city_level1, city_level1_code, city_level2, city_level2_code, city_level3, city_level3_code

    @staticmethod
    def random_datetime(start_datetime: datetime.datetime = None, end_datetime: datetime.datetime = None,
                        fmt='%Y-%m-%d %H:%M:%S.%f') -> datetime.datetime:
        """
        随机生成一个日期
        :param start_datetime: 默认 1940-01-01 00:00:00.00
        :param end_datetime: 默认 now()
        :param fmt:
        :return:
        """
        start_datetime_timestamp = 0 if start_datetime is None else start_datetime.timestamp()
        end_datetime_timestamp = datetime.datetime.now().timestamp() if end_datetime is None else end_datetime.timestamp()

        random_dt = datetime.datetime.fromtimestamp(random.uniform(start_datetime_timestamp, end_datetime_timestamp))

        # str_datetime = random_dt.strftime(fmt=fmt)
        return random_dt

    @staticmethod
    def random_department() -> str:
        return random.choice(all_data_dict["departments"])

    @staticmethod
    def random_phone() -> str:
        """
        随机生成一个11位数的手机号码
        :return:
        """
        phone_pre_list = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151",
                          "152", "153", "155", "156", "157", "158", "159", "186", "187", "188"]
        return random.choice(phone_pre_list) + "".join(random.choice("0123456789") for i in range(8))

    @staticmethod
    def random_email() -> str:
        emailEnd = random.choice(["@qq.com", "@163.com", "@126.com", "@139.com", "@sohu.com", "@aliyun.com", "@189.cn"])

        # 创建一个长度为[3,10)由 字母或数字组成的字符串
        headStr = LzRandomData.random_symbol(random.randint(5, 10), zztsFlag=False, wordFlag=True, numbersFlag=True,
                                             repeat=False)
        email = headStr + emailEnd
        return email

    @staticmethod
    def random_symbol(count=10, zztsFlag=True, wordFlag=True, numbersFlag=True,
                      repeat=True) -> str:
        """
        随机生成一个字符串
        :param count: 字符长度
        :param zztsFlag: 是否包含标点符号
        :param wordFlag: 是否包含单词
        :param numbersFlag: 是否包含数字
        :param repeat: 是否允许出现重复字符
        :return:
        """

        # 特殊字符ASCII码 `~@#...
        zzts = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/',
                ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']

        # 字母ASCII码 abcd...
        words = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

        # 数字ASCII码 012...
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        allSymbol = [zzts, words, numbers]
        allSymbolFlag = [zztsFlag, wordFlag, numbersFlag]
        symbols = []
        for i, e in enumerate(allSymbolFlag):
            if e:
                symbols.extend(allSymbol[i])

        if repeat:
            return "".join(random.choices(symbols, k=count))
        else:
            if count > len(symbols):
                print("非重复的数据过长!")
                return None
            else:
                return "".join(random.sample(symbols, k=count))

    @staticmethod
    def random_chinese_word(count=1, common=True) -> str:
        if common:
            return "".join(random.choices(all_data_dict["commonWords"], k=count))
        else:
            return "".join([chr(random.randint(0x4e00, 0x9fbf)) for i in range(count)])

    @staticmethod
    # 18位身份证号码
    def random_id(city_code: str = None, birth_datetime_code: str = None, sex=None) -> str:
        """
        随机生成一个身份证号码
        :param city_code: 省市县 编码
        :param birth_datetime_code: 出生日期
        :param sex: 性别
        :return:
        """
        sex = random.choice(['男', '女']) if sex is None else sex

        # 地址码6位, 省(2) 市(2) 县/区(2)
        city_code: str = LzRandomData.random_city()[-1] if city_code is None else city_code
        # 出生日期码8位, 年(4) 月(2) 日(2)
        birth_datetime_code: str = LzRandomData.random_datetime().strftime(
            '%Y%m%d') if birth_datetime_code is None else birth_datetime_code

        # 顺序码3位
        sort_code = random.randint(100, 300)
        if (sex == '男') and (sort_code % 2 != 1):
            sort_code += 1
        if (sex == '女') and (sort_code % 2 != 0):
            sort_code += 1
        sort_code = str(sort_code)

        # 校验码1位
        check_code = None

        temp_id = city_code + birth_datetime_code + sort_code
        # 前17位号码权重值
        weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]  # 权重项
        sum_weight = sum(list(map(lambda ele: ele[0] * ele[1], list(zip(list(map(int, list(temp_id))), weight)))))
        check_code_map = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
        check_code = check_code_map[sum_weight % 11]

        user_id_code = temp_id + check_code
        return user_id_code

    @staticmethod
    def random_url() -> str:
        r_str1 = LzRandomData.random_symbol(zztsFlag=False)
        arg_str = '/'.join(
            [LzRandomData.random_symbol(zztsFlag=False, count=random.randint(2, 10)) for i in
             range(0, random.randint(1, 10))])

        URL = f"http://www.{r_str1}.com/{arg_str}"

        return URL


class LzRandomDataTableLine(object):
    @abstractmethod
    def random_data(self): ...

    def to_dict(self):
        var_members = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]
        member_dict = {var: getattr(self, var) for var in var_members}
        return member_dict

    def dict_fill(self, data_dict: dict):
        for k, v in data_dict.items():
            setattr(self, k, v)

    def __str__(self) -> str:
        return str(self.to_dict())


class LzRandomDataTable(object):
    field_comment: LzRandomDataTableLine = None
    table_comment: str = None
    table_data: List[LzRandomDataTableLine] = None
    line: LzRandomDataTableLine = None

    @abstractmethod
    # 设置行数据字段的描述
    def set_table_comment(self):
        ...

    # 生成随机数据
    def random_data(self, num):
        self.table_data = []
        for i in range(num):
            line_data = TableLine().random_data()
            self.table_data.append(line_data)
        return self

    # 设置当前表字段数据从其他表中获取
    def join_master_field(self, master_table: 'LzRandomDataTable', master_table_field: str, this_table_field: str):
        for line in self.table_data:
            m_line = random.choice(master_table.table_data)
            setattr(line, this_table_field, getattr(m_line, master_table_field))

    def to_dataframe(self, columns_as_comment=False) -> pd.DataFrame:
        df = None
        if columns_as_comment is True:
            columns_dict = self.field_comment.to_dict()
            df = pd.DataFrame([{columns_dict[k]: v for k, v in line.to_dict().items()} for line in self.table_data])
        else:
            df = pd.DataFrame([line.to_dict() for line in self.table_data])
        return df

    def __init__(self, table_len: int = 10) -> None:
        self.set_table_comment()
        self.random_data(table_len)

    def __str__(self):
        return str(self.to_dataframe())


class TableLine(LzRandomDataTableLine):
    id_card: str = None
    name_first: str = None
    name_last: str = None
    name: str = None
    sex: str = None
    university: str = None
    education: str = None
    city_level1: str = None
    city_level1_code: str = None
    city_level2: str = None
    city_level2_code: str = None
    city_level3: str = None
    city_level3_code: str = None
    datetime_pre: str = None
    datetime: str = None
    datetime_last: str = None
    department: str = None
    phone_number: str = None
    email: str = None
    chinese_word: str = None
    symbol: str = None
    url: str = None
    age: str = None
    qq_number: str = None

    def __random_add_datetime(self):
        return relativedelta.relativedelta(years=random.randint(0, 100),
                                           months=random.randint(1, 12),
                                           days=random.randint(1, 30),
                                           hours=random.randint(0, 23),
                                           minute=random.randint(1, 59),
                                           seconds=random.randint(0, 59))

    def random_data(self):
        """
        字段随机数据
        :return:
        """
        self.name_first, self.name_last, self.name, self.sex = LzRandomData.random_name_sex()
        fmt = '%Y-%m-%d %H:%M:%S.%f'
        r_dt = LzRandomData.random_datetime()
        p_dt = r_dt - self.__random_add_datetime()
        l_dt = r_dt + self.__random_add_datetime()
        self.datetime = r_dt.strftime(fmt)
        self.datetime_pre = p_dt.strftime(fmt)
        self.datetime_last = l_dt.strftime(fmt)
        self.city_level1, self.city_level1_code, self.city_level2, self.city_level2_code, self.city_level3, self.city_level3_code = LzRandomData.random_city()
        self.id_card = LzRandomData.random_id(city_code=self.city_level3_code,
                                              birth_datetime_code=r_dt.strftime('%Y%m%d'),
                                              sex=self.sex)

        self.university = LzRandomData.random_university()
        self.education = random.choice(['小学', '初中', '高中', '专科', '本科', '硕士', '博士'])

        self.department = LzRandomData.random_department()

        self.phone_number = LzRandomData.random_phone()

        self.email = LzRandomData.random_email()

        self.chinese_word = LzRandomData.random_chinese_word(count=random.randint(3, 15))

        self.symbol = LzRandomData.random_symbol(zztsFlag=False)

        self.url = LzRandomData.random_url()

        self.age = str(random.randint(0, 100))

        self.qq_number = LzRandomData.random_number()

        return self


class Table(LzRandomDataTable):
    table_comment: str = '模板数据表'
    line: TableLine = TableLine()

    def set_table_comment(self):
        """
        字段名注释
        :return:
        """
        self.field_comment = TableLine()
        self.field_comment.id_card = '身份证号'
        self.field_comment.name_first = '姓'
        self.field_comment.name_last = '名'
        self.field_comment.name = '姓名'
        self.field_comment.sex = '性别'
        self.field_comment.university = '大学'
        self.field_comment.education = '学历'
        self.field_comment.city_level1 = '省级名称'
        self.field_comment.city_level1_code = '省级编码'
        self.field_comment.city_level2 = '市级名称'
        self.field_comment.city_level2_code = '市级编码'
        self.field_comment.city_level3 = '县/区级名称'
        self.field_comment.city_level3_code = '县/区级编码'
        self.field_comment.datetime_pre = '日期前'
        self.field_comment.datetime = '日期'
        self.field_comment.datetime_last = '日期后'
        self.field_comment.department = '部门'
        self.field_comment.phone_number = '手机号码'
        self.field_comment.email = '邮箱'
        self.field_comment.chinese_word = '中文汉字'
        self.field_comment.symbol = '字符串'
        self.field_comment.url = '链接'
        self.field_comment.age = '年龄'
        self.field_comment.qq_number = 'QQ号码'


def create_default_code(user: str, password: str, db_name: str, table_name: str):
    """
    根据MySQL数据库表自动生成模板代码
    :param user:
    :param password:
    :param db_name:
    :param table_name:
    :return:
    """
    lzm = LzMySQL(user, password, db_name)
    table_meta = lzm.table_meta_data(table_name)

    table_name = ''
    table_comment = ''
    field_name_comment = {}

    for meta in table_meta:
        table_name = meta['tbname']
        table_comment = meta['tbcomment']

        colcomment = meta['colcomment']
        field_name_comment[meta['colname']] = '' if (colcomment is None) or (colcomment == 'None') else colcomment

    s1 = '        '.join([f'{field}: str = None\n' for field in field_name_comment.keys()])
    s2 = '            '.join([f'self.{field} = None\n' for field in field_name_comment.keys()])
    table_line_code = f"""
    from lazycode.core.tool.LzRandomData import LzRandomDataTableLine,LzRandomDataTable
    class TableLine_{table_name}(LzRandomDataTableLine):
        qq_number: str = None
        {s1}

        def random_data(self):
            {s2}
            return self
    """
    s1 = '            '.join(
        [f'self.field_comment.{field} = "{comment}"\n' for field, comment in field_name_comment.items()])
    table_code = f"""
    class Table_{table_name}(LzRandomDataTable):
        table_comment: str = "{table_comment}"
        line: {f'TableLine_{table_name}'} = {f'TableLine_{table_name}'}()

        def set_table_comment(self):
            self.field_comment = {f'TableLine_{table_name}'}()
            {s1}
    """
    from lazycode.setting import RESOURCE_DIR
    template_code_path = os.path.join(RESOURCE_DIR, 'LzRandomDataTemplateCode.py')
    with open(template_code_path, 'w', encoding='utf-8') as f:
        f.write(lzm.beautiful_string(table_line_code))
        f.write('\n')
        f.write(lzm.beautiful_string(table_code))
        f.write('\n')
    print(f'代码已生成在 {template_code_path}')


# create_default_code('root', '123456', 'information_schema', 'TABLES')


# from lazycode.core.LzDataFrame import LzDataFrameImp
# import os
#
# lz = Table(10)
# lzdf = LzDataFrameImp(lz.to_dataframe())
# csv_txt = lzdf.to_text(have_header=True, column_sep='\t')
# with open(os.path.join(TEMP_DIR, 'random_data.csv'), 'w', encoding='utf-8') as f:
#     f.write(csv_txt)
