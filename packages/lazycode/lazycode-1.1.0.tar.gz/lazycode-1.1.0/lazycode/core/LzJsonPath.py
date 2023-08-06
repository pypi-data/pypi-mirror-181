from enum import Enum
import re
from typing import List, Set, Tuple, Iterator, Dict, Union, Optional
from typing import Any, AnyStr, Callable, NoReturn, ClassVar, Final
from typing import NewType, TypeVar
from lazycode.core.LzNumber import LzNumberImp


class REGS(Enum):
    # 值为 list 的元素
    LIST_ELEMENT_REG = re.compile(r'^\[(.+?)\]$')
    # [1:5:2], [1:5]
    LIST_REG1 = re.compile(r'^(\d*?):(\d*?)(:\d+)?$')
    # [1] , [-1]
    LIST_REG2 = re.compile(r'^(-?\d+)$')
    # [1,2,3]
    LIST_REG3 = re.compile(r'^\d(,\d+)*$')

    # * 或者 book 或者 title,price,color
    DICT_REG = re.compile('^[\w\*]+?(,.*?)*$')

    # (/color).==("red") , (../[:]).list_size.==(10)
    FILTER_REG = re.compile(r'^\((.*?)\)(\..*?)?\.(.*?)\((.*?)\)$')
    # "red"
    FILTER_REG_STRING = re.compile(r'^"(.+?)"$')
    # 10
    FILTER_REG_INT = re.compile(r'^\d+$')
    # 3.14
    FILTER_REG_FLOAT = re.compile(r'^\d+\.\d+$')
    # "red", "blue"
    FILTER_REG_LIST = re.compile(r'^".+?"( *?, *?".+?")+$')
    # findall
    FILTER_REG_LIST_VALUES = re.compile(r'"(.*?)"')


class UtilFunction(object):
    lz_json_path: 'LzJsonPathImp' = None

    def __init__(self, lz_json_path) -> None:
        self.lz_json_path = lz_json_path

    @staticmethod
    def auto_change_type(args):
        res = None
        if re.compile(r'^\d+$').search(args):
            res = int(args)
        elif re.compile(r'^\d+\.\d+$').search(args):
            res = float(args)
        elif re.compile(r'^".*?"$').search(args):
            res = args.strip('"')
        elif re.compile(r'^".+?"( *?, *?".+?")+$').search(args):
            reg = re.compile(r'^".+?"( *?, *?".+?")+$').search(args)
            res = re.compile(r'"(.*?)"').findall(reg.group(0))
        else:
            raise Exception(f'{args} 无法解析')

        return res

    # 处理子路径获取结果的函数
    def switch_function1(self, fun_name1: str, a: List):  # [ /k1/[1], ... ]
        fun_name1 = fun_name1.strip('.')
        if fun_name1 is None:
            return a
        elif fun_name1 == 'one_ele_key':
            # 获取路径最后面的 key
            return a[0].split(self.lz_json_path.sep)[-1]
        elif fun_name1 == 'one_ele_value':
            # 获取路径的值
            return self.lz_json_path.get_value_by_sample_path(a[0])
        elif fun_name1 == 'keys':
            return list(map(lambda ele: ele.split(self.lz_json_path.sep)[-1], a))
        elif fun_name1 == 'list_size':
            # 获取元素的个数
            return len(a)
        else:
            raise Exception(f'{fun_name1} 未定义')

    # 处理比较函数
    def switch_function2(self, fun_name2, a, b):
        if fun_name2 == '>':
            return a > b
        elif fun_name2 == '>=':
            return a >= b
        elif fun_name2 == '<':
            return a < b
        elif fun_name2 == '<=':
            return a <= b
        elif fun_name2 == '==':
            return a == b
        elif fun_name2 == '!=':
            return a != b
        elif fun_name2 == 'like':
            reg = re.compile(b).search(a)
            return True if reg is not None else False
        elif fun_name2 == 'in':
            return a in b
        elif fun_name2 == 'in_left':
            # 右边的元素是否在左边的集合内
            return b in a
        elif fun_name2 == 'nin':
            return a not in b
        elif fun_name2 == 'nin_left':
            return b not in a
        else:
            raise Exception(f'{fun_name2} 无法匹配')

    @staticmethod
    def cat_head_str(path: str, cat_str: str):
        return path.lstrip(cat_str)


class ArgMate(object):
    data = None
    path: str = None

    def __init__(self, data=None, path: str = None) -> None:
        self.data = data
        self.path = path

    def __str__(self) -> str:
        v = None
        if isinstance(self.data, List):
            v = f'List({len(self.data)})'
        elif isinstance(self.data, Dict):
            v = f'Dict({list(self.data.keys())})'
        else:
            v = self.data
        return f'{self.path}:{v}'


class LzJsonPathImp(object):
    """
    # 获取 store 下的 color key
    /store/color
    # 获取store字典所有的 key
    /store/*

    # 跨多级路径查找, 符合... store ... color_type 这样路径的数据
    //store//color_type

    # 获取 book 数组index为 1 的元素, [开始下标:结束下标:步长]
    /store/book/[1]
    /[0]/book/[1]
    /store/book/[:2]
    /store/book/[:]
    /store/book/[::2]
    /store/book/[-1]

    # path_xxx(path): get_value(book[N], path) > >= < <= == != in nin like
    /store/book/[(/color).==("red")]
    /store/book/[(/color).!=("red")]
    /store/book/[(/color).in("red", "blue")]
    /store/book/[(/color).nin("red", "blue")]
    /store/book/[(/color).like("^re.*")]
    /store/book/[(/price).>(10)]
    /store/book/[(/[0]/price).<=(10)]
    /store/book/[(../[:]).list_size.==(10)] # ../[:] 表示父级节点
    """
    base_data: Union[List, Dict] = None
    sep: str = None
    db_sep: str = None
    # __paths: set = set()
    __all_node: set = set()
    __all_base_node: set = set()

    def __init__(self, base_data: Union[Dict, List], sep: str = '/') -> None:
        self.base_data = base_data
        self.sep = sep
        self.db_sep = f'{sep}{sep}'

    def __is_list(self, data) -> bool:
        return isinstance(data, List)

    def __is_dict(self, data) -> bool:
        return isinstance(data, Dict)

    def check_path_exists(self, path: str):
        try:
            self.get_value_by_sample_path(path)
        except Exception as e:
            return False
        return True

    def __path_split(self, path: str):
        #  /*//[1]/key/[(../[:]).list_size.==(10)]
        meta_path_list = []
        tail_path = path
        all_paths = []
        while len(tail_path) > 0:
            seps = re.compile(f'^({self.sep}+)').search(tail_path)
            if seps is not None:
                all_paths.append({
                    'type': 'sep',
                    'value': seps.group(1)
                })
            else:
                raise Exception(f'未识别到 {self.sep}')

            tail_path = tail_path.strip(self.sep)
            sub_path = tail_path.split(self.sep)
            for i in range(len(sub_path)):
                meta_path = self.sep.join(sub_path[:i + 1])
                list_reg = REGS.LIST_ELEMENT_REG.value.search(meta_path)
                dict_reg = REGS.DICT_REG.value.search(meta_path)
                dict_reg_filter = REGS.FILTER_REG.value.search(meta_path)

                if list_reg or dict_reg or dict_reg_filter:
                    all_paths.append({
                        'type': 'key',
                        'value': meta_path
                    })
                    meta_path_list.append(meta_path)
                    tail_path = self.sep.join(sub_path[i + 1:])
                    if tail_path != '':
                        tail_path = self.sep + tail_path
                    break
            else:
                raise Exception(f'{path} 中 {tail_path} 无法解析')
        return meta_path_list, all_paths

    # 路径切分
    def path_split_key(self, path: str):
        meta_path_list, all_paths = self.__path_split(path)
        return meta_path_list

    # data (../[:]).list_size.==(10)
    def __filter_str(self, argmate: ArgMate, string):
        path = argmate.path
        value_path, fun_name1, fun_name2, args = REGS.FILTER_REG.value.search(string).groups()

        # 去除 ..
        pre_meta_path_list = path.split(self.sep)
        sub_path = value_path
        while sub_path.startswith('..'):
            pre_meta_path_list.pop()
            sub_path = sub_path.strip('..')
            if sub_path.strip(self.sep).startswith('..'):
                sub_path = sub_path.strip(self.sep)

        temp_path = self.sep.join(pre_meta_path_list) + sub_path
        # path_exists = self.check_path_exists(temp_path)
        # print(temp_path)
        # if path_exists:
        #     # print(temp_path)
        #     a = self.get_path_burst(temp_path)
        # else:
        #     # print(temp_path)
        #     return False
        a = self.get_path_burst(temp_path)
        a = UtilFunction(self).switch_function1(fun_name1, a)
        b = UtilFunction.auto_change_type(args)
        res_bool = UtilFunction(self).switch_function2(fun_name2, a, b)
        return res_bool

    # data  [1]
    def __get_value(self, data, sample_meta_path):
        list_reg = REGS.LIST_ELEMENT_REG.value.search(sample_meta_path)
        if list_reg is not None:
            index = int(list_reg.group(1))
            return data[index]
        else:
            return data[sample_meta_path]

    # /store/book
    def get_value_by_sample_path(self, path: str, json_data=None):
        path_list = path.strip(self.sep).split(self.sep)
        data = self.base_data if json_data is None else json_data
        for meta_path in path_list:
            data = self.__get_value(data, meta_path)
        return data

    # data [:]
    def __burst_mate_path(self, argmate, meta_path: str):
        # print('11__burst_mate_path', argmate, meta_path)

        data = argmate.data
        path = argmate.path
        meta_path = meta_path.strip()

        list_reg = REGS.LIST_ELEMENT_REG.value.search(meta_path)
        dict_reg = REGS.DICT_REG.value.search(meta_path)
        dict_reg_filter = REGS.FILTER_REG.value.search(meta_path)

        if list_reg is not None and self.__is_list(data):
            # print('list', meta_path)
            # [ ... ]
            list_txt = list_reg.group(1)
            reg1 = REGS.LIST_REG1.value.search(list_txt)
            reg2 = REGS.LIST_REG2.value.search(list_txt)
            reg3 = REGS.LIST_REG3.value.search(list_txt)
            reg4_filter = REGS.FILTER_REG.value.search(list_txt)

            # [1:10:2]
            if reg1 is not None:
                list_len = len(data)
                start = reg1.group(1)
                start = 0 if start is None else 0 if start == '' else int(start)
                end = reg1.group(2)
                end = list_len if end is None else list_len if end == '' else int(end)
                step = reg1.group(3)
                step = step.strip(':') if step is not None else step
                step = 1 if step is None else 1 if step == '' else int(step)
                return [f'{path}{self.sep}[{i}]' for i in range(start, end, step)]

            # [-1]
            elif reg2 is not None:
                index = int(reg2.group(1))
                index = (len(data) + index) if index < 0 else index
                return [f'{path}{self.sep}[{index}]']

            # [1,2,3]
            elif reg3 is not None:
                index_list = list(map(int, reg3.group(0).split(',')))
                return [f'{path}{self.sep}[{index}]' for index in index_list]

            # [(../[:]).list_size.==(10)]
            elif reg4_filter is not None:
                list_len = len(data)
                res = []
                for i in range(list_len):
                    am = ArgMate()
                    am.path = f'{path}{self.sep}[{i}]'
                    # res.append(am.path)
                    am.data = self.get_value_by_sample_path(am.path)
                    # print(list_txt)
                    if self.__filter_str(am, list_txt) is True:
                        res.append(am.path)
                return res
            else:
                raise Exception(f'{list_txt} 无法解析!')
        # key1,key2 , *
        elif dict_reg is not None and self.__is_dict(data):
            # print('dict', meta_path)
            res = []
            if meta_path == '*':
                res = [f'{path}{self.sep}{key}' for key in data.keys()]
            else:
                keys_set = set([f'{path}{self.sep}{key}' for key in data.keys()])
                path_keys = [f'{path}{self.sep}{key}' for key in meta_path.split(',')]
                if len(set(path_keys) - keys_set) == 0:
                    res = path_keys

            return res
        elif dict_reg_filter is not None and self.__is_dict(data):
            res = []
            for key in data.keys():
                am = ArgMate()
                am.path = f'{path}{self.sep}{key}'
                am.data = self.get_value_by_sample_path(am.path)
                res.append(am.path)
            return res
        else:
            # raise Exception(f"无法解析 {meta_path}")
            return []

    def get_path_burst(self, path: str) -> List:
        path_set = set()
        self.__path_burst(ArgMate(self.base_data, ''), path, path_set)
        lis = list(path_set)
        lis.sort()
        return lis

    # def __path_burst2(self, path: str):
    #     meta_path_list, all_paths = self.__path_split(path)
    #
    #     for i, ele in enumerate(all_paths):
    #         ele_type = ele.get('type')
    #         value = ele.get('value')
    #
    #         if ele_type == 'sep':
    #             if value == self.sep:
    #                 pass
    # //k1/k2//k3
    def __path_burst(self, argmate: ArgMate, tail_path: str, path_set: set) -> set:
        """
        表达式条件暂时不可用
        todo /store/book/[(../[:]).list_size.==(10)]
        :param argmate:
        :param tail_path:
        :return:
        """
        # print('in', argmate, tail_path)

        if tail_path == '':
            path_set.add(argmate.path)
            return path_set

        if not (self.__is_dict(argmate.data) or self.__is_list(argmate.data)):
            return path_set

        path = argmate.path
        data = argmate.data

        curr_mate_path = self.path_split_key(tail_path)[0]
        nn_tail_path = UtilFunction.cat_head_str(tail_path.strip(self.sep), curr_mate_path)

        path_list = self.__burst_mate_path(argmate, curr_mate_path)
        # //...
        if tail_path.startswith(self.db_sep):
            all_path = []
            if self.__is_dict(data):
                all_path = self.__burst_mate_path(argmate, '*')
            if self.__is_list(data):
                all_path = self.__burst_mate_path(argmate, '[:]')

            for p in all_path:
                # if (len(path_list) > 0) and (len(set(path_list) - set(all_path)) == 0):
                if p in path_list:
                    # for p in path_list:
                    #     # if deep_all:
                    # for p in all_path:
                    if self.check_path_exists(p):
                        self.__path_burst(ArgMate(self.get_value_by_sample_path(p), p), nn_tail_path, path_set)
                else:
                    # for p in all_path:
                    if self.check_path_exists(p):
                        self.__path_burst(ArgMate(self.get_value_by_sample_path(p), p), tail_path, path_set)

        else:
            for np in path_list:
                if self.check_path_exists(np):
                    self.__path_burst(ArgMate(self.get_value_by_sample_path(np), np), nn_tail_path, path_set)

    def __init_all_node(self):
        self.__all_node.clear()
        self.__all_base_node.clear()
        self.__all_base_element(ArgMate(self.base_data, ''))

    def get_all_base_node(self, flush=False) -> List:
        """
        获取所有的叶子节点
        :param flush: 是否重新获取一次数据
        :return:
        """
        if len(self.__all_base_node) == 0 or flush:
            self.__init_all_node()
        lis = list(self.__all_base_node)
        lis.sort()
        return lis

    def get_all_node(self, flush=False) -> List:
        """
        获取所有节点
        :param flush:
        :return:
        """
        if len(self.__all_base_node) == 0 or flush:
            self.__init_all_node()

        lis = list(self.__all_node)
        lis.sort()
        return lis

    def __all_base_element(self, argmate: ArgMate):
        if argmate.path != '':
            self.__all_node.add(argmate.path)
        else:
            pass
        # print(argmate.path)
        if self.__is_list(argmate.data):
            paths = self.__burst_mate_path(argmate, '[:]')
        elif self.__is_dict(argmate.data):
            paths = self.__burst_mate_path(argmate, '*')
        else:
            # print(self.__all_base_node)
            self.__all_base_node.add(argmate.path)
            return self.__all_base_node
        for p in paths:
            self.__all_base_element(ArgMate(self.get_value_by_sample_path(p), p))

        return self.__all_base_node

    def j_path(self, path: str):
        path_list = self.get_path_burst(path)
        return [self.get_value_by_sample_path(p) for p in path_list]
