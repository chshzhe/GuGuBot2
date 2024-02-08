# import aiosqlite
# from nonebot import logger
#
# from configs.path_config import DATABASE_PATH
#
#
# class AsyncSQLiteDB:
#     def __init__(self, db_path):
#         self.conn = None
#         self.db_path = db_path
#
#     async def connect(self):
#         self.conn = await aiosqlite.connect(self.db_path)
#         await self.conn.execute("PRAGMA foreign_keys = ON")
#         logger.info("Database connection established.")
#
#     async def create_table(self, create_table_sql):
#         async with self.conn.cursor() as cursor:
#             await cursor.execute(create_table_sql)
#             logger.debug(f"Table created: {create_table_sql}")
#             await self.conn.commit()
#
#     async def insert(self, insert_sql, data):
#         async with self.conn.cursor() as cursor:
#             await cursor.execute(insert_sql, data)
#             logger.debug(f"Data inserted: {data}")
#             await self.conn.commit()
#
#     async def query(self, query_sql, data=None):
#         async with self.conn.cursor() as cursor:
#             if data:
#                 await cursor.execute(query_sql, data)
#             else:
#                 await cursor.execute(query_sql)
#             result = await cursor.fetchall()
#             logger.debug(f"Query result: {result}")
#             return result
#
#     async def update(self, update_sql, data):
#         async with self.conn.cursor() as cursor:
#             await cursor.execute(update_sql, data)
#             logger.debug(f"Data updated: {data}")
#             await self.conn.commit()
#
#     async def delete(self, delete_sql, data):
#         async with self.conn.cursor() as cursor:
#             await cursor.execute(delete_sql, data)
#             logger.debug(f"Data deleted: {data}")
#             await self.conn.commit()
#
#     async def close(self):
#         await self.conn.close()
#         logger.info("Database connection closed.")
#
#
# db = AsyncSQLiteDB(DATABASE_PATH + "GuGuBot.db")
import sqlite3

from nonebot import logger

from configs.path_config import DATABASE_PATH


class SQLiteDB:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def connect(self):
        """创建数据库连接"""
        self.conn = sqlite3.connect(self.db_name)
        logger.info("Database connection established.")

    def create_table(self, create_table_sql):
        """创建表"""
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
            logger.debug(f"Table created successfully.")
        except Exception as e:
            logger.error(e)

    def insert(self, insert_sql, data):
        """插入数据"""
        try:
            c = self.conn.cursor()
            c.execute(insert_sql, data)
            self.conn.commit()
            logger.debug("Data inserted successfully.")
        except Exception as e:
            logger.error(e)

    def query(self, query_sql):
        """查询数据"""
        try:
            c = self.conn.cursor()
            c.execute(query_sql)
            results = c.fetchall()
            logger.debug("Data queried successfully.")
            return results
        except Exception as e:
            logger.error(e)
            return None

    def update(self, update_sql, data):
        """更新数据"""
        try:
            c = self.conn.cursor()
            c.execute(update_sql, data)
            self.conn.commit()
            logger.debug("Data updated successfully.")
        except Exception as e:
            logger.error(e)

    def delete(self, delete_sql, data):
        """删除数据"""
        try:
            c = self.conn.cursor()
            c.execute(delete_sql, data)
            self.conn.commit()
            logger.debug("Data deleted successfully.")
        except Exception as e:
            logger.error(e)

    def table_exists(self, table_name):
        """检查表是否存在"""
        c = self.conn.cursor()
        c.execute(f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        if c.fetchone()[0] == 1:
            return True
        else:
            return False

    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed.")


db = SQLiteDB(DATABASE_PATH + "GuGuBot.db")
