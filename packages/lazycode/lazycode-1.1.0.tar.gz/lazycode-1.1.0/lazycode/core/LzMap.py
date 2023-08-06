from typing import List, AnyStr, Any, Tuple
import copy
from lazycode.core.BaseType import BaseType


class LzMapFun1(object):
    # [ ['k1', 'v1'], ['k2','v2] ]
    def convert_element2_to_map(self, arg_list: List[Tuple[AnyStr, Any]]): ...

    def put_item(self, key: str, value: object): ...

    def merge_map(self, other_map: dict): ...

    def remove_item(self, key): ...

    def remove_item_list(self, key_list: list): ...

    def get_value(self, key: str) -> object: ...

    def get_value_default(self, key: str, default_value: object) -> object: ...

    def value_list_by_keys(self, key_list: list) -> list: ...

    def item_list(self) -> list: ...

    def key_list(self) -> list: ...

    def value_list(self) -> list: ...


class LzMap(BaseType, LzMapFun1):
    pass


class LzMapImp(LzMap):
    __map: dict = None
    # ==================================================
    def __init__(self, base_type: dict):
        self.init(base_type=base_type)

    def __str__(self):
        return self.to_string()

    def init(self, base_type: dict):
        self.__map = base_type

    def to_string(self) -> str:
        return str(self.__map)

    def base_type(self):
        return self.__map

    def copy(self):
        return LzMapImp(copy.deepcopy(self.__map))
    # ==================================================
    def convert_element2_to_map(self, arg_list: List[Tuple[AnyStr, Any]]):
        self.__map = dict(arg_list)
        return self

    def put_item(self, key: str, value: object):
        self.__map[key] = value
        return self

    def merge_map(self, other_map: dict):
        self.__map = {**self.__map, **other_map}
        return self

    def remove_item(self, key):
        self.__map.pop(key)
        return self

    def remove_item_list(self, key_list: list):
        for k in key_list:
            self.__map.pop(k)
        return self

    def get_value(self, key: str) -> object:
        return self.__map[key]

    def get_value_default(self, key: str, default_value: object) -> object:
        return self.__map.get(key, default_value)

    def value_list_by_keys(self, key_list: list) -> list:
        value_list = [self.__map[k] for k in key_list]
        return value_list

    def item_list(self) -> list:
        return list(self.__map.items())

    def key_list(self) -> list:
        return list(self.__map.keys())

    def value_list(self) -> list:
        return list(self.__map.values())
