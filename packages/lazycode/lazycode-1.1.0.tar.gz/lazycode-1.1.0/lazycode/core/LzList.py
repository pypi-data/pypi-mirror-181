from collections import Counter
from itertools import product, zip_longest
from functools import reduce
import random
import copy

from lazycode.core.BaseType import BaseType


class LzListFun1(object):
    def length(self) -> int: ...

    def append(self, element: object): ...

    def append_head(self, element: object): ...

    def merge_tail(self, other_list: list): ...

    def insert_element(self, index: int, element: object): ...

    def pop(self) -> object: ...

    def pop_head(self) -> object: ...

    def clear_all(self): ...

    def remove_element_by_index(self, elements_index: list): ...

    def remove_element(self, element: object): ...

    def slice(self, start: int = 0, end: int = None, step: int = 1): ...

    def get(self, index: int) -> object: ...

    def find_element_index(self, element: object) -> list: ...

    def set(self, index: int, value: object): ...

    def reverse_list(self): ...

    def sort_list(self, sort_key_fun: callable = lambda ele: ele, reverse=False): ...


class LzListFun2(object):

    # 统计某个元素的个数
    def count_element(self, element: object) -> int: ...

    # 统计每一个元素的个数
    def counter(self) -> list: ...

    def contains(self, element_list: list) -> bool: ...

    # 元素所有可能的排列组合
    def product(self): ...

    def map(self, fun: callable): ...

    def reduce(self, fun: callable) -> object: ...

    def filter(self, fun: callable): ...

    def all_is_true(self, fun: callable = lambda ele: bool(ele)) -> bool: ...

    def any_is_true(self, fun: callable = lambda ele: bool(ele)) -> bool: ...

    # 如果所有元素的数据类型一致则返回数据的类型
    def all_element_type(self) -> list: ...

    def max_element(self, key_fun: callable = lambda ele: ele) -> object: ...

    def min_element(self, key_fun: callable = lambda ele: ele) -> object: ...

    def sum_element(self) -> object: ...

    def zip_short(self, other_list: list): ...

    def zip_long(self, other_list: list): ...

    def unique_list(self): ...

    # [ [index0, element], [index1, element], ... ]
    def enumerate(self) -> list: ...

    # 或集
    def logic_or(self, other_list: list): ...

    # 差集
    def logic_sub(self, other_list: list): ...

    # 与集
    def logic_and(self, other_list: list): ...

    # 非集
    def logic_not(self, other_list: list): ...

    # 将集合切分为多个子集
    def split_sub_list_by_elenum(self, ele_num: int): ...

    def split_sub_list_by_listnum(self, sub_list_num: int): ...

    # back: 是否放回
    def random_element(self, k=1, back=False, weights: list = None) -> list: ...

    def random_shuffle(self): ...


class LzListFun3(object):

    def element2_to_map(self) -> dict: ...

    def to_set(self, join_str: str) -> str: ...


class LzList(BaseType, LzListFun1, LzListFun2, LzListFun3):
    pass


class LzListImp(LzList):
    __list: list = None

    # ==================================================
    def __init__(self, base_type: list = None):
        self.init(base_type)

    def __str__(self):
        return self.to_string()

    def init(self, base_type: list):
        self.__list = base_type
        return self

    def to_string(self) -> str:
        return str(self.__list)

    def base_type(self):
        return self.__list

    def copy(self):
        return LzListImp(copy.deepcopy(self.__list))

    # ==================================================
    def length(self) -> int:
        return len(self.__list)

    def append(self, element: object):
        self.__list.append(element)
        return self

    def append_head(self, element: object):
        self.__list = [element] + self.__list
        return self

    def merge_tail(self, other_list: list):
        self.__list = self.__list + other_list
        return self

    def insert_element(self, index: int, element: object):
        self.__list.insert(index, element)
        return self

    # ==================================================
    def pop(self) -> object:
        return self.__list.pop()

    def pop_head(self) -> object:
        return self.__list.pop(0)

    def clear_all(self):
        self.__list = []
        return self

    def remove_element_by_index(self, elements_index: list):
        ele_list = [ele for i, ele in enumerate(self.__list) if i not in elements_index]
        self.__list = ele_list
        return self

    def remove_element(self, element: object):
        ele_list = [ele for ele in self.__list if ele != element]
        self.__list = ele_list
        return self

    def slice(self, start: int = 0, end: int = None, step: int = 1):
        self.__list = self.__list[start:end:step]
        return self

    def get(self, index: int) -> object:
        return self.__list[index]

    def find_element_index(self, element: object) -> list:
        ele_index = [i for i, ele in enumerate(self.__list) if ele == element]
        return ele_index

    def set(self, index: int, value: object):
        self.__list[index] = value
        return self

    def reverse_list(self):
        self.__list.reverse()
        return self

    def sort_list(self, sort_key_fun: callable = lambda ele: ele, reverse=False):
        self.__list = list(sorted(self.__list, key=sort_key_fun, reverse=reverse))
        return self

    # ==================================================
    def count_element(self, element: object) -> int:
        return self.__list.count(element)

    def counter(self) -> list:
        ct = Counter(self.__list)
        lis = [[ele, num] for ele, num in dict(ct).items()]
        lis = list(sorted(lis, key=lambda ele: ele[1], reverse=True))
        return lis

    def contains(self, element_list: list) -> bool:
        flag = True
        for ele in element_list:
            if ele not in self.__list:
                flag = False
                break

        return flag

    def product(self):
        # 集合内的元素必须为可迭代对象
        self.__list = list(product(*self.__list, repeat=1))
        return self

    def map(self, fun: callable):
        self.__list = list(map(__func=fun, __iter1=self.__list))
        return self

    def reduce(self, fun: callable) -> object:
        return reduce(fun, self.__list)

    def filter(self, fun: callable):
        self.__list = list(filter(fun, self.__list))
        return self

    def all_is_true(self, fun: callable = lambda ele: bool(ele)) -> bool:
        return all(list(map(fun, self.__list)))

    def any_is_true(self, fun: callable = lambda ele: bool(ele)) -> bool:
        return any(list(map(fun, self.__list)))

    def all_element_type(self) -> list:
        all_type = [str(type(ele)) for ele in self.__list]
        return list(set(all_type))

    def max_element(self, key_fun: callable = lambda ele: ele) -> object:
        element = max(self.__list, key=key_fun)
        return element

    def min_element(self, key_fun: callable = lambda ele: ele) -> object:
        element = min(self.__list, key=key_fun)
        return element

    def sum_element(self) -> object:
        return sum(self.__list)

    def zip_short(self, other_list: list):
        self.__list = list(zip(self.__list, other_list))
        return self

    def zip_long(self, other_list: list):
        self.__list = list(zip_longest(self.__list, other_list))
        return self

    def unique_list(self):
        self.__list = list(set(self.__list))
        return self

    def enumerate(self) -> list:
        return list(enumerate(self.__list))

    def logic_or(self, other_list: list):
        self.__list = self.__list + other_list
        return self

    def logic_sub(self, other_list: list):
        self.__list = [ele for ele in self.__list if ele not in other_list]
        return self

    def logic_and(self, other_list: list):
        self.__list = [ele for ele in self.__list if ele in other_list]
        return self

    def logic_not(self, other_list: list):
        or_list = self.__list + other_list
        and_list = [ele for ele in self.__list if ele in other_list]
        self.__list = [ele for ele in or_list if ele not in and_list]
        return self

    def split_sub_list_by_elenum(self, ele_num: int):
        i = 0
        list_len = len(self.__list)
        res = []
        while i < list_len:
            res.append(self.__list[i: i + ele_num])
            i += ele_num
        self.__list = res
        return self

    def split_sub_list_by_listnum(self, sub_list_num: int):
        index_list = [list(range(i, len(self.__list), sub_list_num)) for i in range(sub_list_num)]
        res = []
        for lis in index_list:
            res.append([self.__list[i] for i in lis])

        self.__list = res
        return self

    def random_element(self, k=1, back=False, weights: list = None) -> list:
        # 不放回
        if back is False:
            return list(random.sample(self.__list, k=k))
        else:
            # weights= [1,1,1,1,...] 默认所有元素权重相同
            return list(random.choices(self.__list, k=k, weights=weights))

    def random_shuffle(self):
        random.shuffle(self.__list)
        return self

    # ==================================================

    # [(k1,v1), (k2,v2), ...] => {k1:v2, k2:v2, ...}
    def element2_to_map(self) -> dict:
        return dict(self.__list)

    def to_set(self, join_str: str) -> str:
        return join_str.join(self.__list)
