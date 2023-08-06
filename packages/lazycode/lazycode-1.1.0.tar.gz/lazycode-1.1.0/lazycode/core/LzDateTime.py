import datetime
from dateutil import relativedelta
from typing import List, Union, AnyStr
import pandas as pd
import re
import calendar
import copy
from lazycode.decorator.decorator import SafeInfo, SafeOperationInClassMethod


class LzDateTimeImp(SafeInfo):
    __datetime: datetime.datetime = None

    def __init__(self, arg_datetime: datetime.datetime = None):
        self.init(arg_datetime)

    def __str__(self):
        return self.to_string()

    def init(self, base_type: datetime.datetime):
        self.__datetime = base_type
        return self

    def base(self) -> datetime.datetime:
        return self.__datetime

    def copy(self):
        return LzDateTimeImp(copy.deepcopy(self.__datetime))

    # YYYY-MM-DD hh:mm:ss.mms
    def to_string(self) -> str:
        year = self.__datetime.year
        month = self.__datetime.month
        day = self.__datetime.day
        hour = self.__datetime.hour
        minute = self.__datetime.minute
        second = self.__datetime.second
        microsecond = self.__datetime.microsecond
        return f'{year:0>4}-{month:0>2}-{day:0>2} {hour:0>2}:{minute:0>2}:{second:0>2}.{microsecond}'

    def convert_datetime_string_format(self, datetime_string: str, format_str: str = '%y-%m-%d %h:%mi:%s.%ms',
                                       year: str = '%y', month: str = '%m', day: str = '%d', hour: str = '%h',
                                       minute: str = '%mi', second: str = '%s', microsecond: str = '%ms'):

        rp_dic = dict(
            minute=(minute, r'(\d{1,2})'),
            microsecond=(microsecond, r'(\d+)'),

            year=(year, r'(\d{4})'),
            month=(month, r'(\d{2})'),
            day=(day, r'(\d{2})'),
            hour=(hour, r'(\d{1,2})'),
            second=(second, r'(\d{1,2})'),
        )
        default_value_dic = dict(
            year=1, month=1, day=1,
            hour=0, minute=0, second=0, microsecond=0
        )
        temp_lis = []
        format_str_cp = format_str
        for name, (k, v) in rp_dic.items():

            # 使用等长空白字符占位已经搜索过的区域
            fi = format_str_cp.find(k)
            if fi != -1:
                temp_lis.append((name, fi))
            format_str_cp = format_str_cp.replace(k, ' ' * len(k))

            # 将特殊占位符替换为正则字符
            format_str = format_str.replace(k, v)
        temp_lis = list(sorted(temp_lis, key=lambda ele: ele[1]))
        temp_lis = [ele[0] for ele in temp_lis]
        values = re.compile(f'^{format_str}$').search(datetime_string).groups()

        dic = dict(zip(temp_lis, values))
        data_dic = {**default_value_dic, **dic}
        data_dic = {k: int(v) for k, v in data_dic.items()}
        self.__datetime = datetime.datetime(**data_dic)
        return self

    # 1668779590.000123 秒
    def convert_timestamp(self, timestamp: float):
        self.__datetime = datetime.datetime.fromtimestamp(timestamp)
        return self

    # 时间戳(秒)
    def timestamp(self) -> float:
        return self.__datetime.timestamp()

    # 时间戳(秒) 10位
    def timestamp_s(self) -> int:
        timestamp = self.__datetime.timestamp()
        return int(timestamp)

    # 时间戳(毫秒) 13位
    def timestamp_ms(self) -> int:
        timestamp = self.__datetime.timestamp()
        return int(round(timestamp * 1000))

    # 时间戳(微秒) 16位
    def timestamp_mms(self) -> int:
        timestamp = self.__datetime.timestamp()
        return int(round(timestamp * 1000000))

    @SafeOperationInClassMethod()
    def now(self):
        self.__datetime = datetime.datetime.now()
        return self

    @SafeOperationInClassMethod()
    def add_datetime(self, years=0, months=0, days=0, weeks=0, hours=0, minutes=0, seconds=0, microseconds=0):
        self.__datetime = self.__datetime + relativedelta.relativedelta(years=years, months=months, days=days,
                                                                        weeks=weeks, hours=hours, minutes=minutes,
                                                                        seconds=seconds, microseconds=microseconds)
        return self

    @SafeOperationInClassMethod()
    def sub_datetime(self, years=0, months=0, days=0, weeks=0, hours=0, minutes=0, seconds=0, microseconds=0):
        self.__datetime = self.__datetime - relativedelta.relativedelta(years=years, months=months, days=days,
                                                                        weeks=weeks, hours=hours, minutes=minutes,
                                                                        seconds=seconds, microseconds=microseconds)
        return self

    def week_of_year(self) -> int:
        # 如果当前年的第一周和上一年的最后一周有重叠时,
        # 得到的结果是上一年的所属上一年的周数
        weeks = pd.to_datetime(self.__datetime).weekofyear
        if weeks > 5 and self.__datetime.month < 2:
            print("注意: 当前日期所属周, 与上一年存在重叠!")
            weeks = 0
        return weeks

    def day_of_year(self) -> int:
        return pd.to_datetime(self.__datetime).day_of_year

    def day_of_week(self) -> int:
        return pd.to_datetime(self.__datetime).day_of_week + 1

    @SafeOperationInClassMethod()
    def monday(self, n: int = 0):
        n = n - 1
        # 获取周一日期, 0 表示下一周周一
        self.__datetime = self.__datetime + relativedelta.relativedelta(weekday=relativedelta.MO(n))
        return self

    @SafeOperationInClassMethod()
    def sunday(self, n: int = 0):
        n = n - 1
        # 获取周日日期, 0 表示下一周周日
        self.__datetime = self.__datetime + relativedelta.relativedelta(weekday=relativedelta.SU(n))
        return self

    @SafeOperationInClassMethod()
    def end_datetime_in_month(self):
        end_day = pd.to_datetime(self.__datetime).days_in_month
        diff_day = end_day - self.__datetime.day
        self.__datetime = self.__datetime + relativedelta.relativedelta(days=diff_day)
        return self

    @SafeOperationInClassMethod()
    def start_datetime_in_month(self):
        self.__datetime = self.__datetime - relativedelta.relativedelta(days=self.__datetime.day - 1)
        return self

    def month_calendar(self) -> List[List]:
        """
        本月二维数组日历
        :return:
        """
        # 数组中0表示空白日期
        return calendar.monthcalendar(self.__datetime.year, self.__datetime.month)

    # [ start : end ]
    def datetime_range(self, start_datetime: Union[AnyStr, datetime.datetime],
                       end_datetime: Union[AnyStr, datetime.datetime],
                       step_type: AnyStr = 'D') -> List[datetime.datetime]:
        # Y: 年, M: 月, D: 日, W: 周, Q: 季度, H: 时, T: 分, S: 秒, L: 毫秒
        # 所生成的区间范围的最后日期 <= end_date
        if isinstance(start_datetime, str):
            start_datetime = datetime.datetime.strptime(start_datetime, '%Y-%m-%d %H:%M:%S.%f')
        if isinstance(end_datetime, str):
            end_datetime = datetime.datetime.strptime(end_datetime, '%Y-%m-%d %H:%M:%S.%f')

        datetime_list = pd.date_range(start_datetime, end_datetime, freq=step_type)
        datetime_list = [datetime.datetime.fromtimestamp(date.timestamp()) for date in datetime_list]
        return datetime_list

    def is_week_start(self) -> bool:
        # 本周一日期
        dt = self.__datetime + relativedelta.relativedelta(weekday=relativedelta.MO(-1))
        return self.__datetime == dt

    def is_week_end(self) -> bool:
        # 本周日日期
        dt = self.__datetime + relativedelta.relativedelta(weekday=relativedelta.SU(-1))
        return self.__datetime == dt

    def is_month_start(self) -> bool:
        return pd.to_datetime(self.__datetime).is_month_start

    def is_month_end(self) -> bool:
        """
        是否为月末日期
        :return:
        """
        return pd.to_datetime(self.__datetime).is_month_end

    def is_quarter_start(self) -> bool:
        """
        是否为季度开始日期
        :return:
        """
        return pd.to_datetime(self.__datetime).is_quarter_start

    def is_quarter_end(self) -> bool:
        """
        是否为季度结束日期
        :return:
        """
        return pd.to_datetime(self.__datetime).is_quarter_end

    def year(self) -> int:
        return self.__datetime.year

    def month(self) -> int:
        return self.__datetime.month

    def day(self) -> int:
        return self.__datetime.day

    def hour(self) -> int:
        return self.__datetime.hour

    def minute(self) -> int:
        return self.__datetime.minute

    def second(self) -> int:
        return self.__datetime.second

    def microsecond(self) -> int:
        return self.__datetime.microsecond


print(LzDateTimeImp().datetime_range(
    '2022-1-1 12:10:10.0',
    '2022-1-1 12:10:20.0',
    step_type='S'
))
