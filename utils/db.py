import sqlite3
from typing import Optional, List, Tuple

from nonebot import logger


class SQLiteDB:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def get_conn(self) -> sqlite3.Connection:
        """获取数据库连接"""
        return self.conn

    def connect(self) -> None:
        """创建数据库连接"""
        self.conn = sqlite3.connect(self.db_name)
        logger.info("Database connection established.")

    def create_table(self, create_table_sql) -> None:
        """创建表"""
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
            logger.debug(f"Table created successfully.")
        except Exception as e:
            logger.error(e)

    def insert(self, insert_sql, data) -> None:
        """插入数据"""
        try:
            c = self.conn.cursor()
            c.execute(insert_sql, data)
            self.conn.commit()
            logger.debug("Data inserted successfully.")
        except Exception as e:
            logger.error(e)

    def query(self, query_sql) -> Optional[List[Tuple]]:
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

    def update(self, update_sql, data) -> None:
        """更新数据"""
        try:
            c = self.conn.cursor()
            c.execute(update_sql, data)
            self.conn.commit()
            logger.debug("Data updated successfully.")
        except Exception as e:
            logger.error(e)

    def delete(self, delete_sql, data) -> None:
        """删除数据"""
        try:
            c = self.conn.cursor()
            c.execute(delete_sql, data)
            self.conn.commit()
            logger.debug("Data deleted successfully.")
        except Exception as e:
            logger.error(e)

    def table_exists(self, table_name) -> bool:
        """检查表是否存在"""
        c = self.conn.cursor()
        c.execute(f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        if c.fetchone()[0] == 1:
            return True
        else:
            return False

    def close(self) -> None:
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed.")
