import os
import shutil
import datetime
import inspect
from lazycode.decorator.decorator import SafeInfo, SafeOperationInClassMethod


class LzFileDirImp(SafeInfo):
    __path: str = None

    def __init__(self, path: str = None):
        self.init(path)

    def __str__(self) -> str:
        return self.to_string()

    def init(self, path: str):
        self.__path = path

    def to_string(self) -> str:
        return self.__path

    def copy(self):
        return LzFileDirImp(self.__path)

    def get_class_file_path(self, obj: object):
        """
        获取对象类所在的文件路径
        :param obj:
        :return:
        """
        self.__path = inspect.getfile(obj.__class__)
        return self

    def make_file(self) -> bool:
        """
        创建文件
        :param encoding:
        :return:
        """
        os.mknod(self.__path)
        return True

    def read_content(self, mode='r', encoding='utf-8') -> object:
        """
        读取文件内容
        :param mode:
        :param encoding:
        :return:
        """
        content = None
        with open(file=self.__path, mode=mode, encoding=encoding) as f:
            content = f.read()
        return content

    def write_content(self, content, mode='w', encoding='utf-8') -> bool:
        """
        向文件内写入内容
        :param content:
        :param mode:
        :param encoding:
        :return:
        """
        with open(file=self.__path, mode=mode, encoding=encoding) as f:
            f.write(content)
        return True

    def make_dirs(self) -> bool:
        """
        创建多级目录
        :return:
        """
        os.makedirs(self.__path)
        return True

    def check_file_or_dir_exists(self) -> bool:
        """
        检查文件或目录是否存在
        :return:
        """
        return os.path.exists(self.__path)

    def is_file(self) -> bool:
        """
        是否为文件
        :return:
        """
        return os.path.isfile(self.__path)

    def is_dir(self) -> bool:
        """
        是否为目录
        :return:
        """
        return os.path.isdir(self.__path)

    def rename_file_or_dir(self, new_name: str) -> bool:
        """
        重命名文件或目录
        :param new_name:
        :return:
        """
        new_name = os.path.join(os.path.dirname(self.__path), new_name)
        os.rename(self.__path, new_name)
        return True

    def remove_file_dir(self) -> bool:
        """
        删除文件或目录
        :return:
        """
        if os.path.isfile(self.__path):
            os.remove(self.__path)
        else:
            shutil.rmtree(self.__path)

        return True

    def abspath(self) -> str:
        """
        获取绝对路径
        :return:
        """
        return os.path.abspath(self.__path)

    def join(self, *paths: str) -> str:
        """
        路径拼接
        :param path:
        :return:
        """
        path = self.__path
        for p in paths:
            path = os.path.join(path, p)
        return path

    def split_dir_file(self) -> list:
        """
        切分父级目录和文件名
        :return:
        """
        return list(os.path.split(self.__path))

    def base_dir_path(self) -> str:
        """
        获取文件袋父级目录路径
        :return:
        """
        return os.path.dirname(self.__path)

    def get_filename(self) -> str:
        """
        获取文件名
        :return:
        """
        return os.path.split(self.__path)[1]

    def get_filename_not_suffix(self) -> str:
        """
        获取文件名, 去掉文件类型后缀
        :return:  file
        """
        return os.path.splitext(os.path.split(self.__path)[1])[0]

    def get_drive(self) -> str:
        """
        获取路径盘符驱动名
        :return: D:
        """
        return os.path.splitdrive(self.__path)[0]

    def get_suffix(self) -> str:
        """
        获取文件类型后缀
        :return: .txt
        """
        return os.path.splitext(self.__path)[1]

    # 获取文件, 大小(字节)
    def file_info_filesize(self) -> int:
        return os.stat(self.__path).st_size

    # 文件最后访问 时间
    def file_info_lvtime(self) -> str:
        timestamp = os.stat(self.__path).st_atime
        return datetime.datetime.fromtimestamp(timestamp).strftime(fmt='%Y-%m-%d %H:%M:%S.%f')

    # 文件最后修改 时间
    def file_info_lmtime(self) -> str:
        timestamp = os.stat(self.__path).st_mtime
        return datetime.datetime.fromtimestamp(timestamp).strftime(fmt='%Y-%m-%d %H:%M:%S.%f')

    # 文集创建时间
    def file_info_lctime(self) -> str:
        timestamp = os.stat(self.__path).st_ctime
        return datetime.datetime.fromtimestamp(timestamp).strftime(fmt='%Y-%m-%d %H:%M:%S.%f')

    def deep_copy_file(self, to_path: str) -> bool:
        """
        深度复制文件, 包括修改时间
        :param to_path:
        :return:
        """
        shutil.copy2(self.__path, to_path)
        return True

    def list_dir_files(self) -> list:
        return os.listdir(self.__path)

    def walk(self) -> list:
        """
        递归获取目录下的文件和目录, 包含三个参数 (当前目录路径, 当前目录下的所有目录, 当前目录下的所有文件)
        :return:
        """
        return list(os.walk(self.__path))

    def deep_walk_all_file(self) -> list:
        """
        获取目录下所有的文件和目录
        :return:
        """
        all_file = []
        for path, dirs, files in os.walk(self.__path):
            all_file.append(path)
            all_file.extend([os.path.join(path, f) for f in files])
        return all_file

# lz = LzFileDirImp()
# print(lz.get_class_file_path(BaseType()).split_dir_file())
