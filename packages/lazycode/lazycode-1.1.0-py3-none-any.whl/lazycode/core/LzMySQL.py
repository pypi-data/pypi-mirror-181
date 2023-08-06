import pymysql
from typing import List
import pandas as pd
import re


# # 数据于列名称对其，不错行
# pd.set_option('display.unicode.ambiguous_as_wide', True)
# pd.set_option('display.unicode.east_asian_width', True)
# # 显示所有列
# pd.set_option('display.max_columns', None)
# # 限制最多显示10行数据, 设置None表示全部显示
# pd.set_option('display.max_rows', 10)


class LzMySQL(object):
    __connect: pymysql.Connection = None
    __cursor: pymysql.cursors.Cursor = None
    __dbname: str = None

    def __init__(self, user: str, password: str, db: str,
                 host: str = 'localhost', port: int = 3306, charset: str = 'utf8'):
        self.__dbname = db
        self.init(host=host, user=user, password=password, db=db, port=port, charset=charset)

    def init(self, user: str, password: str, db: str,
             host: str = 'localhost', port: int = 3306, charset: str = 'utf8'):
        self.__connect = pymysql.connect(host=host, user=user, password=password, db=db, port=port, charset=charset)
        self.__cursor = self.__connect.cursor()

    def close(self):
        self.__cursor.close()
        self.__connect.close()

    def execute_transaction(self, sql: str, args: List = None) -> int:
        res = None
        try:
            res = self.__cursor.execute(sql, args)
            self.__connect.commit()
        except Exception as e:
            print(f'{sql} 语句执行失败, 事务回滚')
            self.__connect.rollback()
        return res

    def executemany_transaction(self, sql: str, args: List[List] = None) -> int:
        res = None
        try:
            res = self.__cursor.executemany(sql, args)
            self.__connect.commit()
        except Exception as e:
            print(f'{sql} 语句执行失败, 事务回滚')
            self.__connect.rollback()

        return res

    def query(self, sql: str, args: List = None) -> List:
        line_num = self.__cursor.execute(sql, args)

        res_data = []
        if line_num > 0:
            self.__connect.commit()
            data_line = self.__cursor.fetchall()

            # 获取列字段元数据信息
            col_infos = self.__cursor.description
            col_names = [col[0] for col in col_infos]
            res_data = [dict(zip(col_names, line)) for line in data_line]
        return res_data

    def query_to_df(self, sql: str, args: List = None) -> pd.DataFrame:
        data = self.query(sql, args)
        df = pd.DataFrame(data)
        return df

    def table_meta_data(self, like_table_reg='%'):
        sql = f'''
        SELECT
            a.TABLE_SCHEMA as dbname, -- 0 数据库名
            a.TABLE_NAME as tbname,     -- 1 表名
            b.TABLE_COMMENT tbcomment,  -- 2 表注释

            a.COLUMN_NAME as colname,       -- 3 列名
            a.COLUMN_COMMENT as colcomment, -- 4 列注释
            a.DATA_TYPE as col_datatype,    -- 5 数据类型
            a.COLUMN_TYPE as coltype,       -- 6 列数据类型(全)
            a.IS_NULLABLE as isnull,        -- 7 是否可以为空
            a.ORDINAL_POSITION as  col_position,    -- 8 列所在位置
            c.CONSTRAINT_NAME as cs_type,   -- 9 列约束类型 PRIMARY, ... 
            c.COLUMN_NAME as cs_col_name,   -- 10 约束列名
            c.REFERENCED_TABLE_SCHEMA as cs_dbname,      -- 11 外键主表数据库名
            c.REFERENCED_TABLE_NAME as cs_tbname,        -- 12 外键主表表名
            c.REFERENCED_COLUMN_NAME as cs_tb_col_name 	 -- 13 外键主表关联列名
        FROM
            (
            SELECT * FROM information_schema.COLUMNS WHERE TABLE_SCHEMA= "{self.__dbname}" -- 数据库名
            ) AS a
        LEFT JOIN information_schema.TABLES AS b
            ON a.TABLE_NAME=b.TABLE_NAME AND a.TABLE_SCHEMA=b.TABLE_SCHEMA
        LEFT JOIN information_schema.KEY_COLUMN_USAGE as c
            ON c.CONSTRAINT_SCHEMA = a.TABLE_SCHEMA 
                AND c.TABLE_NAME = a.TABLE_NAME 
                AND c.COLUMN_NAME = a.COLUMN_NAME
        WHERE a.TABLE_NAME like "{like_table_reg}" -- 需要选择的表格, 默认全部表格
        order by a.TABLE_NAME, a.ORDINAL_POSITION 
        ;
        '''

        return self.query(sql)

    def beautiful_string(self, string):
        # 美化格式
        space = re.search(' *', string.split('\n')[1]).group(0)
        string = '\n'.join(
            [re.sub(r'^' + space, '', line) for line in string.split('\n') if len(line.strip()) > 0])
        return string

# lz = LzMySQL(user='root', password='123456', db='ssm_db')
# # data_lines = lz.query_to_df(
# #     sql='select * from tbl_user',
# # )
# # print(data_lines.columns)
#
# print(pd.DataFrame(lz.table_meta_data()))
