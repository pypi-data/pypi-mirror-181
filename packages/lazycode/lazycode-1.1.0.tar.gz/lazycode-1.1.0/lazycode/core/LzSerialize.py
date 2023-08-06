import pickle


class LzSerialize(object):

    @staticmethod
    def dump_to_file(obj: object, file_path: str) -> None:
        """
        序列化对象并写到文件
        :param obj:
        :param file_path:
        :return:
        """
        with open(file_path, mode='wb') as f:
            pickle.dump(obj, f)

    @staticmethod
    def dump(obj: object) -> bytes:
        """
        序列化对象
        :param obj:
        :return:
        """
        return pickle.dumps(obj)

    @staticmethod
    def load_from_file(file_path: str) -> object:
        """
        反序列化文件内容
        :param file_path:
        :return:
        """
        res = None
        with open(file_path, mode='rb') as f:
            res = pickle.load(f)
        return res

    @staticmethod
    def load(data: bytes) -> object:
        """
        反序列化
        :param data:
        :return:
        """
        return pickle.loads(data)

#
# dic = {
#     'k1': 'v1',
#     'k2': 'v2'
# }
# # LzSerialize.dump_to_file(dic, './temp.pk')
#
# print(LzSerialize.load_from_file('./temp.pk'))
#
