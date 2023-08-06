from typing import List, Dict
from pymongo import MongoClient, database, collection
import re


class LzMongoDBImp(object):
    client: MongoClient = None
    db: database.Database = None
    db_collection: collection.Collection = None

    # 数据库, 数据表(集合), 不需要创建, 在插入数据时会自动创建
    def __init__(self, db_name, arg_collection, host='127.0.0.1', port=27017) -> None:
        self.client = MongoClient(host=host, port=port)
        self.db = self.client.get_database(db_name)
        self.db_collection = self.db.get_collection(arg_collection)

    def list_collection_names(self) -> List[str]:
        return self.db.list_collection_names()

    def insert_many_data(self, data_list: List[Dict]) -> List:
        return self.db_collection.insert_many(data_list).inserted_ids

    def find(self, where: dict = None, need_fields: list = None):
        need_fields = {} if need_fields is None else {field: 1 for field in need_fields}

        where = {} if where is None else where
        """
        正则: { 'name': '/^Go/' }
        比较: { 'age': { '$gt': 10} }; 映射 >: $gt, >=: $gte: , <: $lt, <=: $lte, !=: $ne
        集合: { 'age': {'$in': [ 10, 12,15] } };  包含: $in, 不包含: $nin
        逻辑: and { 'name': '李四', 'age': 12}; or { '$or' : [{'name': '李四'}, {'age': 15}] }
        """
        find_result = self.db_collection.find(where, need_fields)
        return find_result

    def update(self, where, update_dict):
        # self.db_collection.update_many({'name':'/^G/'}, {'$set': {'age': 18}})
        return self.db_collection.update_many(where, update_dict)

    def remove(self, where):
        # self.db_collection.delete_many({'name': '/^G/'})
        return self.db_collection.delete_many(where)
# data_store = {
#     'db1': {  # db1 数据库
#         'table1': [  # 数据表(集合)
#             {  # 第一条数据
#                 '_id': 1,
#                 'name': '李四'
#             },
#             {  # 二条数据
#                 '_id': 2,
#                 'name': '李四'
#             },
#         ]
#     }
# }
#
# lz = LzMongoDBImp('db1', 'tb1')
#
# # line_data1 = lz.db_collection.insert_one({"name": "Google", "alexa": "1", "url": "https://www.google.com"})
# # line_data2 = lz.db_collection.insert_many([
# #     {"name": "Taobao", "alexa": "100", "url": "https://www.taobao.com"},
# #     {"name": "QQ", "alexa": "101", "url": "https://www.qq.com"},
# #     {"name": "Facebook", "alexa": "10", "url": "https://www.facebook.com"},
# #     {"name": "知乎", "alexa": "103", "url": "https://www.zhihu.com"},
# #     {"name": "Github", "alexa": "109", "url": "https://www.github.com"}
# # ])
# # print(line_data1.inserted_id)
# # print(line_data2.inserted_ids)
#
# print(lz.db_collection.find_one())
# print(list(lz.db_collection.find()))
# print(list(lz.db_collection.find({}, {"_id": 0, "name": 1, "alexa": 1})))
