import copy
import time
from functools import wraps
from abc import abstractmethod


class SafeInfo(object):
    """
    通过继承 SafeInfo 类, 让装饰器可以识别
    """
    __var_open_safe = True

    def open_safe(self):
        self.__var_open_safe = True
        return self

    def close_safe(self):
        self.__var_open_safe = False
        return self

    def get_safe(self) -> bool:
        return self.__var_open_safe

    def deep_copy_obj(self):
        return copy.deepcopy(self)


class SafeOperationInClassMethod(object):
    """
    使用位置: 添加在类方法上
    作用: 在类方法调用时, 会先创建一个新的实例对象再调用这个对象的类方法
    注意: 直接在类内部实例化的变量, 无法进行深度复制
    """

    def __call__(self, fun):  # 接受函数
        @wraps(fun)
        def wrapper(*args, **kwargs):
            # 获取类实例对象
            sf = args[0]
            if sf.get_safe() is True:
                # 复制一个新的实例对象
                # new_instance = getattr(args[0], self.__copy_fun_name)()
                # new_instance = copy.deepcopy(sf)
                new_instance = sf.deep_copy_obj()
                # 将新的实例对象作为参数传入
                args = (new_instance, *args[1:])
            # 执行函数, 返回执行结果
            return fun(*args, **kwargs)

        return wrapper  # 返回函数


class RunTimePrint(object):
    def __call__(self, fun):
        def wrapper(*args, **kwargs):
            start = time.time()
            res = fun(*args, **kwargs)
            end = time.time()

            runtime = end - start
            print(f'running time [ {runtime} s] detail function => {fun}')
            return res

        return wrapper
