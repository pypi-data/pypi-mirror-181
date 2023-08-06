import datetime
from threading import Timer
from typing import Callable, Dict
import pandas as pd
import re
import time
import sys
import os
import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

fmt = "%Y-%m-%d %H:%M:%S"


class TaskMeta(object):
    start_datetime: datetime.datetime = None
    end_datetime: datetime.datetime = None

    task_name: str = None
    task: Callable = None
    args = None
    kwargs = None

    year_str = None
    month_str = None
    day_str = None
    week_str = None
    hour_str = None
    minute_str = None
    second_str = None

    def __init__(self, task_name, task: Callable, args=None, kwargs=None,
                 start_datetime=None, end_datetime=None,
                 second='*', minute='*', hour='*', day='*',
                 month='*', week='*', year='*'
                 ) -> None:
        """

        :param task: 任务函数
        :param args:
        :param kwargs:
        :param start_datetime: 任务开始时间, 默认立即开始
        :param end_datetime: 任务结束时间
        :param second:
            * 每秒执行一次
            0 表示不使用当前时间类型
            */2 每2秒执行一次
            2,5,10 第2,5,10秒时执行一次
            2-5 在 2,3,4,5 秒时执行一次
            10-40/2 在10-40秒时每隔2秒执行一次
        :param minute:
        :param hour:
        :param day:
        :param month:
        :param week:
        :param year:
        :return:
        """
        self.task_name = task_name
        self.start_datetime = start_datetime if start_datetime is not None else datetime.datetime.now()
        self.end_datetime = end_datetime if end_datetime is not None else datetime.datetime(year=9999, month=1, day=1)
        self.task = task
        self.args = args if args is not None else ()
        self.kwargs = kwargs if kwargs is not None else {}

        self.year_str = year
        self.month_str = month
        self.day_str = day
        self.hour_str = hour
        self.minute_str = minute
        self.second_str = second
        self.week_str = week

    def convert(self, time_str: str, time_range: list, expect: int):
        reg1 = re.compile(r'^\*/(\d{1,2})$').search(time_str)
        reg2 = re.compile(r'^(\d{1,4})(,\d{1,4})*$').search(time_str)
        reg3 = re.compile(r'^(\d{1,4})-(\d{1,4})$').search(time_str)
        reg4 = re.compile(r'^(\d{1,4})-(\d{1,4})/(\d{1,4})$').search(time_str)
        time_str = time_str.strip()
        if time_str == '*':
            return expect
        elif time_str == '0':
            return time_range[0]
        elif reg1 is not None:
            step = int(reg1.group(1))
            if expect in time_range[::step]:
                return expect
            return None
        elif reg2 is not None:
            times = list(map(int, time_str.split(',')))
            if expect in times:
                return expect
            return None
        elif reg3 is not None:
            start, end = int(reg3.group(1)), int(reg3.group(2))
            times = list(range(start, end + 1))
            if expect in times:
                return expect
            return None
        elif reg4 is not None:
            start, end = int(reg4.group(1)), int(reg4.group(2))
            times = list(range(start, end + 1))
            step = int(reg4.group(3))
            if expect in list(times[start:end:step]):
                return expect
            return None
        else:
            raise Exception(f'{time_str} 格式无法识别')

    def get_datetime_tuple(self):
        now_datetime = datetime.datetime.now()
        week_day = self.convert(self.week_str, list(range(1, 8)), pd.to_datetime(now_datetime).day_of_week + 1)
        expect_day = self.convert(self.day_str, list(range(1, pd.to_datetime(now_datetime).days_in_month + 1)),
                                  now_datetime.day)
        if week_day is None:
            expect_day = None

        return (
            self.convert(self.year_str, list(range(2020, 9999)), now_datetime.year),
            self.convert(self.month_str, list(range(1, 13)), now_datetime.month),
            expect_day,
            self.convert(self.hour_str, list(range(0, 24)), now_datetime.hour),
            self.convert(self.minute_str, list(range(0, 60)), now_datetime.minute),
            self.convert(self.second_str, list(range(0, 60)), now_datetime.second),
        )

    def equals_datetime(self, arg_datetime: datetime.datetime):
        now_datetime_tuple = (arg_datetime.year, arg_datetime.month, arg_datetime.day,
                              arg_datetime.hour, arg_datetime.minute, arg_datetime.second)
        schedule_datetime_tuple = self.get_datetime_tuple()
        if now_datetime_tuple == schedule_datetime_tuple:
            return True
        else:
            return False

    def execute_schedule(self):
        now_datetime = datetime.datetime.now()
        now_datetime = datetime.datetime(year=now_datetime.year, month=now_datetime.month, day=now_datetime.day,
                                         hour=now_datetime.hour, minute=now_datetime.minute, second=now_datetime.second)
        if now_datetime < self.start_datetime:
            print(f'{self.task_name} 还达到任务的开始日期, 任务开始日期为: {self.start_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")}')
            return True
        if now_datetime > self.end_datetime:
            print(f'{self.task_name} 任务已过期, 任务结束日期为: {self.end_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")}')
            return False

        if self.equals_datetime(datetime.datetime.now()) is True:
            print(f'{self.task_name} start running')
            res = self.task(*self.args, **self.kwargs)
            return {'result': res}
        else:
            return True


class LzSchedulerImp(object):
    __scheduler_dict: Dict[str, TaskMeta] = dict()
    fmt = "%Y-%m-%d %H:%M:%S"

    # *(秒) *(分) *(时) *(日) *(月) *(周) *(年)
    # */5 * * * * * * 每5秒执行一次
    def add_schedule_task_str(self, times_str: str, task_name, task: Callable, args=None, kwargs=None,
                              start_datetime_str: str = None, end_datetime_str: str = None):
        times_list = times_str.strip().split(' ')
        start_datetime = None
        end_datetime = None
        # 2022-12-01 10:12:11
        if start_datetime_str is not None:
            start_datetime = datetime.datetime.strptime(start_datetime_str, self.fmt)
        if end_datetime_str is not None:
            end_datetime = datetime.datetime.strptime(end_datetime_str, self.fmt)
        self.add_schedule_task(task_name, task, args, kwargs, start_datetime, end_datetime, *times_list)

    def add_schedule_task(self, task_name, task: Callable, args=None, kwargs=None,
                          start_datetime: datetime = None, end_datetime: datetime.datetime = None,
                          second='*', minute='*', hour='*', day='*',
                          month='*', week='*', year='*'):
        start_datetime = start_datetime if start_datetime is not None else datetime.datetime.now()
        end_datetime = end_datetime if end_datetime is not None else datetime.datetime(year=9999, month=1, day=1)
        args = args if args is not None else ()
        kwargs = kwargs if kwargs is not None else {}

        if start_datetime > end_datetime:
            raise Exception(f'开始日期({start_datetime}) 不能大于 结束日期({end_datetime})')
        taskmeta = TaskMeta(task_name, task, args, kwargs,
                            start_datetime, end_datetime,
                            second, minute, hour, day, month, week, year)
        self.__scheduler_dict[task_name] = taskmeta

    def run(self):
        while True:
            for task_name, task in self.__scheduler_dict.copy().items():
                res = task.execute_schedule()
                if res is False:
                    self.__scheduler_dict.pop(task_name)
            # print(f'running {datetime.datetime.now().strftime(self.fmt)}')

            if len(self.__scheduler_dict) == 0:
                print(f'全部任务已完成!')

            time.sleep(1)


class Tasks(object):

    @staticmethod
    def run_command(command: str):
        logging.info(f'运行 "{command}" 命令')
        os.system(command)


# lz = LzSchedulerImp()
# # lz.add_schedule_task(task_name='task1', task=Tasks().task1, args=('abc',))
# # lz.add_schedule_task(task_name='task2', task=Tasks().task1, args=('def',))
# lz.add_schedule_task_str(times_str='*/2 * * * * * *', task_name='task3', task=Tasks().task1, args=('ghi',),
#                          start_datetime_str='2022-12-05 15:24:10',
#                          end_datetime_str='2022-12-06 17:29:10'
#                          )
#
# lz.run()


if __name__ == '__main__':
    argv = sys.argv
    if len(argv) > 1:
        times_str = argv[1]
        command = ' '.join(argv[2:])
        lzs = LzSchedulerImp()
        lzs.add_schedule_task_str(times_str=times_str, task_name='', task=Tasks.run_command, args=(command,))
        lzs.run()

# python LzScheduler.py "*/2 * * * * * *" "dir ."
