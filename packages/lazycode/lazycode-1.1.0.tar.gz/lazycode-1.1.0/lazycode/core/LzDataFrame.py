from lazycode.decorator.decorator import SafeInfo, SafeOperationInClassMethod

from functools import reduce
import json
import pandas as pd
from enum import Enum
import copy
import re
from typing import List, Dict, Iterable, Optional, AnyStr, Union, Tuple, Any, Callable

# 数据于列名称对其，不错行
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
# 显示所有列
pd.set_option('display.max_columns', None)
# 限制最多显示10行数据, 设置None表示全部显示
pd.set_option('display.max_rows', 10)


class FunctionEnum(Enum):
    APPLY_FUN_FUN: str = "APPLY_FUN_FUN"
    APPLY_FUN_DATA: str = "APPLY_FUN_DATA"

    FILTER_MAP: str = 'FILTER_MAP'
    UPDATE_DATA_MAP: str = 'UPDATE_DATA_MAP'


class DataFrameFunctions(object):
    __data_dict: dict = dict()

    def set(self, key: str, value: object):
        self.__data_dict[key] = value

    def get_data_dict(self):
        return self.__data_dict

    def apply_fun(self, series):
        fun = self.__data_dict[FunctionEnum.APPLY_FUN_FUN]
        apply_fun_data = self.__data_dict.get(FunctionEnum.APPLY_FUN_DATA, None)
        index = series.axe_type
        data_dict = series.to_dict()
        data_dict = fun(index, data_dict, apply_fun_data)
        r_series = pd.Series(data_dict)
        r_series.name = index
        return r_series

    def update_row_data_fun(self, series: pd.Series):
        index = series.name
        series_dict = series.to_dict()
        full_series_dict = {"__index__": index, **series_dict}
        FILTER_MAP = self.__data_dict.get(FunctionEnum.FILTER_MAP, None)
        UPDATE_DATA_MAP = self.__data_dict.get(FunctionEnum.UPDATE_DATA_MAP, None)
        need_update = False
        if FILTER_MAP:
            for fk, fv in FILTER_MAP.items():
                if isinstance(fv, list):
                    if full_series_dict[fk] in fv:
                        need_update = True
                        break
                else:
                    if fv == full_series_dict[fk]:
                        need_update = True
                        break
        if need_update:
            keys = UPDATE_DATA_MAP.keys()
            for k in keys:
                if k not in series_dict.keys():
                    UPDATE_DATA_MAP.pop(k)
            series_dict = {**series_dict, **UPDATE_DATA_MAP}
            series = pd.Series(series_dict)
            series.name = index
        return series


class LzDataFrameImp(SafeInfo):
    __dataframe: pd.DataFrame = None

    def __init__(self, base_type: pd.DataFrame = None):
        self.init(base_type)

    def __str__(self):
        return self.to_string()

    def init(self, base_type: pd.DataFrame):
        self.__dataframe = base_type

    def to_string(self) -> str:
        return str(self.__dataframe)

    def base(self):
        return self.__dataframe

    def copy(self):
        return LzDataFrameImp(copy.deepcopy(self.__dataframe))

    def convert_list(self, data_list: list):
        self.__dataframe = pd.DataFrame(data_list).T
        return self

    def convert_map(self, data_map: dict):
        self.__dataframe = pd.DataFrame(data_map).T
        return self

    def convert_file_text(self, file_path, encoding='utf-8', column_sep: str = ',',
                          first_line_is_column_name: bool = False):
        data_text = ''
        with open(file_path, 'r', encoding=encoding) as f:
            data_text = f.read()
        return self.convert_text(data_text, column_sep, first_line_is_column_name)

    def convert_text(self, data_text: str, column_sep: str = ',', first_line_is_column_name: bool = False):
        data_list = [line.split(column_sep) for line in data_text.split('\n')]
        columns = None
        if first_line_is_column_name:
            columns = data_list[0]
            data_list = data_list[1:]
        self.__dataframe = pd.DataFrame(data_list, columns=columns)
        return self

    def convert_json(self, data_json: str):
        self.__dataframe = pd.DataFrame(json.loads(data_json)).T
        return self

    def values_to_list(self) -> list:
        return self.__dataframe.values.tolist()

    def to_map(self) -> dict:
        return self.__dataframe.T.to_dict()

    def to_file(self, file_path: str, encoding='utf-8', have_header: bool = True, column_sep: str = ',') -> None:
        text = self.to_text(have_header, column_sep)
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(text)

    def to_text(self, have_header: bool = True, column_sep: str = ',') -> str:
        data_list = self.__dataframe.values.tolist()
        if have_header:
            data_list = [self.__dataframe.columns.tolist()] + data_list
        data_list = [column_sep.join(list(map(str, line))) for line in data_list]
        return '\n'.join(data_list)

    def to_json(self) -> str:
        return json.dumps(self.__dataframe.T.to_dict(), ensure_ascii=False)

    @SafeOperationInClassMethod()
    def index_to_column(self, new_column_name: str = 'index_column'):
        self.__dataframe[new_column_name] = self.__dataframe.index
        return self

    @SafeOperationInClassMethod()
    def column_to_index(self, column_name: str):
        self.__dataframe.index = self.__dataframe[column_name]
        self.__dataframe = self.__dataframe.drop([column_name], axis=1)
        return self

    def head(self, n: int) -> pd.DataFrame:
        return self.__dataframe.head(n)

    def tail(self, n: int) -> pd.DataFrame:
        return self.__dataframe.tail(n)

    def loc_mix(self, index_name_list: list = None, column_name_list: list = None,
                i_index_list: list = None, i_column_list: list = None,
                i_index_start: int = None, i_index_end: int = None,
                i_column_start: int = None, i_column_end: int = None
                ) -> pd.DataFrame:
        return LzDataFrameImp(self.loc(index_name_list, column_name_list)) \
            .iloc(i_index_list, i_column_list,
                  i_index_start, i_index_end,
                  i_column_start, i_column_end
                  )

    def iloc(self, i_index_list: list = None, i_column_list: list = None,
             i_index_start: int = None, i_index_end: int = None,
             i_column_start: int = None, i_column_end: int = None) -> pd.DataFrame:
        if i_index_list:
            if i_column_list:
                return self.__dataframe.iloc[i_index_list, i_column_list]
            else:
                return self.__dataframe.iloc[i_index_list, i_column_start:i_column_end]
        else:
            if i_column_list:
                return self.__dataframe.iloc[i_index_start:i_index_end, i_column_list]
            else:
                return self.__dataframe.iloc[i_index_start:i_index_end, i_column_start:i_column_end]

    def loc(self, index_name_list: list = None, column_name_list: list = None):
        if index_name_list:
            if column_name_list:
                return self.__dataframe.loc[index_name_list, column_name_list]
            else:
                return self.__dataframe.loc[index_name_list, :]
        else:
            if column_name_list:
                return self.__dataframe.loc[:, column_name_list]
            else:
                return self.__dataframe.loc[:, :]

    def rows_data_list(self) -> List[Tuple[Any, Dict]]:
        return list(self.__dataframe.T.to_dict().items())

    def columns_data_list(self) -> list:
        return list(self.__dataframe.to_dict().items())

    def get_column_value(self, column_name: str) -> dict:
        return self.__dataframe.loc[:, column_name].to_dict()

    def get_index_value(self, index_name: object) -> dict:
        return self.__dataframe.loc[index_name, :].to_dict()

    @SafeOperationInClassMethod()
    def rename_column(self, column_name_map: dict):
        self.__dataframe = self.__dataframe.rename(columns=column_name_map)
        return self

    @SafeOperationInClassMethod()
    def rename_index(self, index_name_map: dict):
        self.__dataframe = self.__dataframe.rename(index=index_name_map)
        return self

    @SafeOperationInClassMethod()
    def drop_index_column(self):
        self.__dataframe = self.__dataframe.reset_index(drop=True)
        return self

    @SafeOperationInClassMethod()
    def add_or_replace_column(self, column_name: str, column_data: object):
        self.__dataframe[column_name] = column_data
        return self

    @SafeOperationInClassMethod()
    def drop_column(self, column_name: Union[AnyStr, List]):
        if isinstance(column_name, str):
            column_name = [column_name]
        self.__dataframe = self.__dataframe.drop(labels=column_name, axis=1)
        return self

    @SafeOperationInClassMethod()
    def drop_index_row(self, index_name: Union[AnyStr, List]):
        if isinstance(index_name, str):
            index_name = [index_name]
        self.__dataframe = self.__dataframe.drop(labels=index_name, axis=0)
        return self

    @SafeOperationInClassMethod()
    def apply_row(self, fun: callable, fun_data: object = None):
        '''
        fun(index, data_dict, apply_fun_data) ->  data_dict: ...
        '''
        df_fun = DataFrameFunctions()
        df_fun.set(FunctionEnum.APPLY_FUN_FUN, fun)
        df_fun.set(FunctionEnum.APPLY_FUN_DATA, fun_data)
        self.__dataframe = self.__dataframe.apply(df_fun.apply_fun, axis=1)
        return self

    @SafeOperationInClassMethod()
    def apply_column(self, fun: callable, fun_data: object = None):
        df_fun = DataFrameFunctions()
        df_fun.set(FunctionEnum.APPLY_FUN_FUN, fun)
        df_fun.set(FunctionEnum.APPLY_FUN_DATA, fun_data)
        self.__dataframe = self.__dataframe.apply(df_fun.apply_fun, axis=0)
        return self

    @SafeOperationInClassMethod()
    def merge_df_into_row(self, dataframe: Union[pd.DataFrame, List]):
        if isinstance(dataframe, pd.DataFrame):
            dataframe = [dataframe]
        df_list = [self.__dataframe] + dataframe
        columns_list = [df.columns.tolist() for df in df_list]
        self.__dataframe = pd.concat(df_list, axis=1, ignore_index=True)
        columns = []
        for i, ele_list in enumerate(columns_list):
            for column_name in ele_list:
                if column_name not in columns:
                    columns.append(column_name)
                else:
                    columns.append(f'{column_name}_df{i}')
        self.__dataframe.columns = columns
        return self

    @SafeOperationInClassMethod()
    def merge_df_into_column(self, dataframe: Union[pd.DataFrame, List], ignore_column_name: bool = False):
        if isinstance(dataframe, pd.DataFrame):
            dataframe = [dataframe]
        df_list = [self.__dataframe] + dataframe

        if ignore_column_name:
            new_df_list = []
            for df in df_list:
                df = df.copy()
                df.columns = [f'col_{i}' for i in range(len(df.columns.tolist()))]
                new_df_list.append(df)
            df_list = new_df_list

        columns_list = [df.columns.tolist() for df in df_list]
        self.__dataframe = pd.concat(df_list, axis=0, ignore_index=True)
        return self

    @SafeOperationInClassMethod()
    def join(self, dataframe: Union[pd.DataFrame, List], on_column: Union[AnyStr, List], how="inner"):
        """
        两个表 根据字段进行 join
        :param dataframe:
        :param on_column:
        :param how: inner、outer、left、right
        :return:
        """
        if isinstance(dataframe, pd.DataFrame):
            dataframe = [dataframe]
        if isinstance(on_column, str):
            on_column = [on_column]

        join_df = self.__dataframe.copy()
        join_df_list = []
        columns = join_df.columns.tolist()
        for i, df in enumerate(dataframe):
            curr_columns = df.columns
            new_curr_columns = []
            for column in curr_columns:
                if column not in on_column and column in columns:
                    column = f'{column}_{i + 1}'
                new_curr_columns.append(column)
            df = df.copy()
            df.columns = new_curr_columns
            join_df_list.append(df)

        for df in join_df_list:
            join_df = pd.merge(join_df, df, on=on_column, how=how)
        self.__dataframe = join_df
        return self

    def group_by(self, by_columns: Union[AnyStr, List]) -> List:
        """
        对字段数据进行分组
        :param by_columns:
        :return:
            [
                ((v1,v2,...), pd.DataFrame),
                ((v1,v3,...), pd.DataFrame),
                ...
            ]
        """
        if isinstance(by_columns, str):
            by_columns = [by_columns]
        gb_list = list(self.__dataframe.groupby(by=by_columns))
        return gb_list

    @SafeOperationInClassMethod()
    def filter_row(self, filter_map: Dict):
        '''
        :param filter_map: 字典内元素为需要保留的元素
            {'column1' : ['v1','v2','v3',...], 'column2': 'v' }
        :return:
        '''
        filter_bool = []
        for col, data in filter_map.items():
            if isinstance(data, list):
                filter_bool.append(self.__dataframe[col].isin(data))
            else:
                filter_bool.append(self.__dataframe[col] == data)
        filter_bool = list(reduce(lambda pre, next: pre & next, filter_bool))
        self.__dataframe = self.__dataframe[filter_bool]
        return self

    @SafeOperationInClassMethod()
    def filter_row_apply(self, fun: callable, fun_data: object = None):
        '''
        fun(index, data_dict, apply_fun_data) -> bool: ...
        '''
        df_fun = DataFrameFunctions()
        df_fun.set(FunctionEnum.APPLY_FUN_FUN, fun)
        df_fun.set(FunctionEnum.APPLY_FUN_DATA, fun_data)
        need_list = self.__dataframe.apply(df_fun.apply_fun, axis=1).values.tolist()
        need_list = [ele[0] for ele in need_list]
        self.__dataframe = self.__dataframe.loc[need_list, :]
        return self

    @SafeOperationInClassMethod()
    def update_row_data(self, filter_map: dict, update_data_map: dict = None):
        '''
        :param filter_map: 筛选出需要更新的数据行, __index__表示索引列 {'__index__': [0,1,2], 'column1': ['v1', 'v2'], 'column2': 'v3' }
        :param update_data_map:
        :return:
        '''
        df_fun = DataFrameFunctions()
        df_fun.set(FunctionEnum.FILTER_MAP, filter_map)
        df_fun.set(FunctionEnum.UPDATE_DATA_MAP, update_data_map)
        self.__dataframe = self.__dataframe.apply(df_fun.update_row_data_fun, axis=1)
        return self

    @SafeOperationInClassMethod()
    def column_apply(self, column_name: AnyStr, fun: Callable[[Any], Any]):
        """
        对列中每一个元素应用函数
        :param column_name:
        :param fun:
        :return:
        """
        self.__dataframe[column_name] = self.__dataframe[column_name].apply(fun)
        return self

    @SafeOperationInClassMethod()
    def column_astype(self, column: str, fun_astype: Callable):
        return self.column_apply(column_name=column, fun=fun_astype)

    def index_name_list(self) -> list:
        return self.__dataframe.index.tolist()

    def column_name_list(self) -> list:
        return self.__dataframe.columns.tolist()

    @SafeOperationInClassMethod()
    def T(self):
        self.__dataframe = self.__dataframe.T
        return self

    def row_number(self) -> int:
        return len(self.__dataframe.index.tolist())

    def shape(self) -> list:
        index_len = len(self.__dataframe.index.tolist())
        column_len = len(self.__dataframe.columns.tolist())
        return [index_len, column_len]

    @SafeOperationInClassMethod()
    def clear(self):
        self.__dataframe = pd.DataFrame(columns=self.__dataframe.columns.tolist())
        return self

    @SafeOperationInClassMethod()
    def burst_row_apply(self, fun: Callable[[Any, Dict], List[Dict]] = None):
        row_data_list = self.rows_data_list()
        burst_list = []
        for index, row_data in row_data_list:
            lis = fun(index, row_data)
            burst_list.extend(lis)
        df = pd.DataFrame(burst_list)
        self.__dataframe = df
        return self

    @SafeOperationInClassMethod()
    def burst_row_iterable_column(self, column_name: AnyStr):
        return self.burst_row_apply(
            lambda index, row_data: [{**row_data, **{column_name: ele}} for ele in row_data[column_name]])

# from lazycode.setting import RESOURCE_PATH
# import os
#
# lzdf1 = LzDataFrameImp().convert_file_text(os.path.join(RESOURCE_PATH, 'random_data.csv'), column_sep='\t',
#                                            first_line_is_column_name=True)
# lzdf1 = lzdf1.column_to_index('symbol')
# lzdf1 = LzDataFrameImp(lzdf1.iloc(i_index_end=5))
# lzdf1 = lzdf1.add_or_replace_column('aaggee', None)
# # lzdf1 = lzdf1.drop_column('age')
#
# lzdf2 = LzDataFrameImp().convert_file_text(os.path.join(RESOURCE_PATH, 'random_data.csv'), column_sep='\t',
#                                            first_line_is_column_name=True)
# lzdf2 = lzdf2.column_to_index('symbol')
#
# # print(lzdf2.burst_row(
# #     lambda index, row_data: [{**row_data, **{'education': ele}} for ele in re.findall(r'\w', row_data['education'])]))
#
# print(lzdf2.group_by('education'))
