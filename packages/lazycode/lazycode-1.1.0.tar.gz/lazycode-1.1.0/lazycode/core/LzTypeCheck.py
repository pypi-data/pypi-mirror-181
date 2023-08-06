from enum import Enum
from typing import List, Set, Tuple, Iterator, Dict, Union, Optional, Callable
from inspect import signature, Parameter


def function_input_arg_check(function: Callable, *args, **kwargs):
    """
    list , dict, set, str, int, float
    强制类型检查, 注意暂时不支持 typing中的数据类型
    :param function:
    :param args:
    :param kwargs:
    :return:
    """
    sig = signature(function).parameters

    input_args_list = list(args)

    for default_arg_name, pt in sig.items():

        value = None
        value_class = None
        value_default_class = pt.annotation
        if len(input_args_list) > 0:
            value = input_args_list.pop(0)
            value_class = value.__class__
        else:
            if default_arg_name in kwargs:
                value = kwargs.get(default_arg_name)
                value_class = value.__class__

        if (value is None) or (value_class is None):
            continue
        if issubclass(value_default_class, Parameter.empty):
            continue
        else:
            if not issubclass(value_class, value_default_class):
                print(f'参数 {default_arg_name} 期望一个 {value_default_class} 类型数据, 但是传入的 {value} 数据是一个 {value_class} 类型')

        # # 默认值
        # # print(pt.default)
        # # 参数名 : 参数类型 Class
        # default_kwargs_dict[pt.name] = pt.annotation


# from typing import List, Set, Tuple, Iterator, Dict, Union, Optional
# from typing import Any, AnyStr, Callable, NoReturn, ClassVar, Final
# from typing import NewType, TypeVar
#
#
# class LzTypeCheck(object):
#
#     def check_data_structure(self, structure: Union[List, Dict], data: Union[List, Dict]):
#         pass
#
#
# class StructureDataType(Enum):
#     AnyStr = 'AnyStr'
#     Int = 'Int'
#     Float = 'Float'
#     Bool = 'Bool'
#     Null = 'Null'
#
#     # 可有可无
#     Optional = 'Optional'
#
#     # 可以为其中任意一种
#     Union = 'Union'
#
#
# structure = {
#     'name': 'AnyStr',  # 必须有的 key
#     'age': 'Int',
#     'city_code': 'Union[ AnyStr, Int ]',
#     'Optional[key1]': {
#         'Optional[*]': [
#             {
#                 'k1': 'v1',
#             },
#             [
#
#             ]
#         ]
#
#     },
#     'Optional[*]': {
#
#     },
# }
