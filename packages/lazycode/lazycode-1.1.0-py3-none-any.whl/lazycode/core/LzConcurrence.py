from typing import Callable
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing
import asyncio
from functools import partial


# 单CPU多任务并行运行
class MyThread(threading.Thread):
    result = None
    task: threading.Thread = None

    def __init__(self, fun, *args, **kwargs):
        super(MyThread, self).__init__()
        self.fun = fun
        self.args = args
        self.kwargs = kwargs

    # 调用 start 会回调run方法运行线程
    def run(self) -> None:
        self.result = self.fun(*self.args, **self.kwargs)

    # 获取线程的执行结果
    def get_result(self):
        self.join()
        # threading.Thread.join(self)  # 等待线程执行完毕
        return self.result


# # 多CPU多任务并行运行
# class MyProcess(multiprocessing.Process):
#
#     def __init__(self, fun, share_var: multiprocessing.Manager().dict = None, *args, **kwargs):
#         super(MyProcess, self).__init__()
#         self.fun = fun
#         self.args = args
#         self.kwargs = kwargs
#         self.share_var = share_var
#         print(self)
#
#     # 调用 start 会回调run方法运行线程
#     def run(self):
#         print(self)
#         self.share_var['value'] = self.fun(*self.args, **self.kwargs)


class LzConcurrentImpThreading(object):
    __task: MyThread = None

    def create_threading(self, fun: Callable, *args, **kwargs):
        task = MyThread(fun, *args, **kwargs)
        self.__task = task
        return self

    def threading_start(self):
        self.__task.start()
        return self

    def get_threading_result(self):
        return self.__task.get_result()


class LzConcurrentImpThreadingPool(object):
    __threading_pool: ThreadPoolExecutor = None
    __task_dict: dict = {}

    def create_threading_pool(self, max_workers=3):
        self.__threading_pool = ThreadPoolExecutor(max_workers=max_workers)
        return self

    def get_task_by_name(self, task_name: str):
        return self.__task_dict[task_name]

    def add_task_to_threading_pool(self, fun: Callable, task_name: str, *args, **kwargs):
        task = self.__threading_pool.submit(fun, *args, **kwargs)
        self.__task_dict[task_name] = task
        return self

    def get_threading_pool_result(self, task_name: str = None):
        result_dict = {}
        task_name_list = list(self.__task_dict.keys())
        as_completed_list = list(as_completed([self.__task_dict[name] for name in task_name_list]))
        if task_name is None:
            for name, task in zip(task_name_list, as_completed_list):
                result = task.result()
                result_dict[name] = result
        else:
            result_dict[task_name] = as_completed(self.__task_dict[task_name])

        return result_dict

    def shutdown_threading_pool(self):
        self.__threading_pool.shutdown(True)


class LzConcurrentImpProcessing(object):
    __task: multiprocessing.Process = None
    __share_dict = None

    def function(self, share_dict, fun: Callable, args, kwargs):
        share_dict['result'] = fun(*args, **kwargs)

    def set_share_dict(self, share_dict):
        self.__share_dict = share_dict
        return self

    def create_processing(self, fun: Callable, *args, **kwargs):
        task = multiprocessing.Process(target=self.function, args=(self.__share_dict, fun, args, kwargs))
        self.__task = task
        return self

    def processing_start(self):
        self.__task.start()
        return self

    def get_processing_result(self):
        self.__task.join()
        return self.__share_dict['result']


class LzConcurrentImpProcessingPool(object):
    __processing_pool: multiprocessing.Pool = None
    __task_dict: dict = {}

    def create_processing_pool(self, processes=3):
        self.__processing_pool = multiprocessing.Pool(processes=processes)
        return self

    def get_task_by_name(self, task_name: str):
        return self.__task_dict[task_name]

    def add_task_to_processing_pool(self, fun: Callable, task_name: str, *args, **kwargs):
        task = self.__processing_pool.apply_async(fun, args=args, kwds=kwargs)
        self.__task_dict[task_name] = task
        return self

    def get_processing_pool_result(self):
        self.__processing_pool.close()
        self.__processing_pool.join()
        result_dict = {}

        for name, task in self.__task_dict.items():
            result = task.get()
            result_dict[name] = result

        return result_dict


class LzConcurrentAsync(object):
    __loop = asyncio.get_event_loop()
    __task_dict: dict = {}
    __future_task_dict: dict = {}

    # def create_event_loop(self):
    #     self.__loop = asyncio.get_event_loop()

    def _callback_function(self, fun: Callable, args, future):
        return fun(*args)

    def add_task(self, task_name: str, task: Callable, *args, **kwargs):
        self.__task_dict[task_name] = task(*args, **kwargs)
        return self

    def add_task_with_run(self, task_name: str, task: Callable, *args, **kwargs):
        self.add_task(task_name, task, *args, **kwargs)
        self.run_task(task_name)
        return self

    def run_task(self, task_name: str, callback: Callable = None, callback_arg=None):
        async_task = asyncio.ensure_future(self.__task_dict[task_name])

        if callback is not None:
            # 回调函数只能采用位置参数, partial( 回调函数, 参数1, 参数2, ...) 最后一个参数必须是future
            async_task.add_done_callback(partial(self._callback_function, callback, callback_arg))

        # async_task.add_done_callback(partial(callback, *callback_arg))
        self.__future_task_dict[task_name] = async_task
        return self

    def get_task_result(self, task_name: str):
        self.__loop.run_until_complete(self.__future_task_dict[task_name])
        return self.__future_task_dict[task_name].result()

    def get_task_result_all(self):
        tasks = list(self.__future_task_dict.values())
        self.__loop.run_until_complete(asyncio.wait(tasks))

        result_dict = {task_name: task.result() for task_name, task in self.__future_task_dict.items()}
        return result_dict

# class AsyncTasks:
#     """
#     这是最终我们想要的实现.
#     """
#
#     async def sleep(self, name, stime):
#         for i in range(1, stime + 1):
#             print(f"{name} run {i}s {time.time()}")
#             await asyncio.sleep(1)
#
#     async def washing1(self, ):
#         await self.sleep('fun1', 3)  # 使用 asyncio.sleep(), 它返回的是一个可等待的对象
#         print('washer1 finished')
#         return 'washing1'
#
#     async def washing2(self, ):
#         await self.sleep("fun2", 2)
#         print('washer2 finished')
#         return 'washing2'
#
#     async def washing3(self, ):
#         await self.sleep("fun3", 5)
#         print('washer3 finished')
#         return 'washing3'
#
#     def callback(self, arg1, arg2, kwarg1, kwarg2):
#         print(f'callback function {arg1} {arg2} {kwarg1} {kwarg2}')
#         return 'result callback'
#
#
# def func(arg1, arg2):
#     print(arg1, arg2)
#     stime = random.randint(2, 5)
#     print(f'sleep time is {stime}')
#     time.sleep(stime)
#     return arg1, arg2
#
#
# if __name__ == '__main__':
#     t = time.time()
#
#     # lz1 = LzConcurrentImpThreading().create_threading(func, 1, 2).threading_start()
#     # lz2 = LzConcurrentImpThreading().create_threading(func, 3,4).threading_start()
#     # print(lz1.get_threading_result())
#     # print(lz2.get_threading_result())
#     #
#     # lz = LzConcurrentImpThreadingPool()
#     # lz.create_threading_pool()\
#     #     .add_task_to_threading_pool(func, 't1', 1, 2)\
#     #     .add_task_to_threading_pool(func, 't2', 3, 4)\
#     #     .add_task_to_threading_pool(func, 't3', 5, 6)\
#     #     .add_task_to_threading_pool(func, 't4', 7, 8)
#     # print(lz.get_threading_pool_result())
#
#     # share_dict = multiprocessing.Manager().dict()
#     # lz1 = LzConcurrentImpProcessing().set_share_dict(share_dict).create_processing(func, 1, 2).processing_start()
#     # lz2 = LzConcurrentImpProcessing().set_share_dict(share_dict).create_processing(func, 3, 4).processing_start()
#     # print(lz1.get_processing_result())
#     # print(lz2.get_processing_result())
#
#     # lz1 = LzConcurrentImpProcessingPool().create_processing_pool() \
#     #     .add_task_to_processing_pool(func, 'p1', 1, 2) \
#     #     .add_task_to_processing_pool(func, 'p2', 3, 4) \
#     #     .add_task_to_processing_pool(func, 'p3', 5, 6) \
#     #     .add_task_to_processing_pool(func, 'p4', 7, 8)
#     # print(lz1.get_processing_pool_result())
#
#     tk = AsyncTasks()
#     lz = LzAsync()
#     # lz.add_and_run_async_function('tk1', tk.washing1) \
#     #     .add_and_run_async_function('tk2', tk.washing2) \
#     #     .add_and_run_async_function('tk3', tk.washing3)
#     #
#     # print('res: ', lz.get_task_result('tk1'))
#
#     lz.add_async_function('tk1', tk.washing1)
#     lz.run_task('tk1', tk.callback, callback_arg=('tk1 callback', 2, 3, 4))
#     lz.add_async_function('tk2', tk.washing2)
#     lz.run_task('tk2', tk.callback, callback_arg=('tk2 callback', 1, 2, 3))
#
#     lz.wait_all_finished_and_get_result()
#
#     print(time.time() - t)
