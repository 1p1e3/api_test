from typing import Any, Dict, List, Optional, Union, cast
from dbutils.pooled_db import PooledDB
import pymysql
from pymysql.cursors import DictCursor
from pymysql.connections import Connection
from config.settings import settings
from utils.logger import logger

class MySQLClient:

    _pool: Optional[PooledDB] = None

    def __init__(self,
                 host: Optional[str] = None,
                 port: Optional[int] = None,
                 database: Optional[str] = None,
                 user: Optional[str] = None,
                 password: Optional[str] = None,
                 ):
        pool_config = {
            'maxconnections': 10,    # 连接池最大连接数
            'mincached': 3,
            'maxcached': 5,
            'blocking': True
        }

        # 连接池单例
        if MySQLClient._pool is None:
            MySQLClient._pool = PooledDB(
                creator=pymysql,
                cursorclass=DictCursor,
                **pool_config,
                host=host or settings.MYSQL_HOST,
                port=port or settings.MYSQL_PORT,
                database=database or None,
                user=user or settings.MYSQL_USER,
                password=password or settings.MYSQL_PASSWORD,
                )
        
        self.conn = None
        self.cursor = None
    
    # 实现上下文管理器操作
    def __enter__(self):
        self.conn = cast(Connection, MySQLClient._pool.connection())
        self.cursor = self.conn.cursor()
        logger.info('获取数据库连接')
        return self
    

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()

        if self.conn:
            self.conn.close()   # 归还连接

        logger.info('归还数据库连接到连接池')


    @classmethod
    def close_pool(cls):
        """手动关闭连接池"""
        if cls._pool is not None:
            try:
                cls._pool.close()
                logger.info('连接池关闭成功')
            except Exception as e:
                logger.error(f'关闭连接池时出错: {e}')
            finally:
                cls._pool = None
        else:
            logger.warning('连接池未初始化或已关闭')
        
    

    def query_one(self, sql: str, params: Union[tuple, list, dict] = None) -> Optional[Dict]:
        """查询单条数据

        Args:
            sql (str): 要执行的 SQL 语句
            params (Union[tuple, list, dict], optional): 绑定到 SQL 语句中的参数
                - 若为列表或元组， SQL 中使用 `%s` 占位
                - 若为字典, SQL 中使用 `%(name)s` 占位

                默认为 None

        Returns:
            Optional[Dict]: 返回字典形式的结果或 None
        
        Example:
            >>> client.query_one('SELECT * FROM t_user_info WHERE id = %s', (1,))

            {'id': 1, 'name': 'ozymandias'}
        """
        self.cursor.execute(sql, params)
        return self.cursor.fetchone()

    def query_all(self, sql: str, params: Union[tuple, list, dict] = None) -> List[Dict]:
        """查询多条数据

        Args:
            sql (str): 要执行的 SQL 语句
            params (Union[tuple, list, dict], optional): 绑定到 SQL 语句中的参数
                - 若为列表或元组， SQL 中使用 `%s` 占位
                - 若为字典, SQL 中使用 `%(name)s` 占位

                默认为 None

        Returns:
            List[Dict]: 返回字典形式的结果集（列表）或 None
        """
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()


    def query_value(self, sql: str, params: Union[tuple, list, dict] = None) -> Any:
        """查询单个值, 如 COUNT、MAX 等函数的结果

        Args:
            sql (str): 要执行的 SQL 语句
            params (Union[tuple, list, dict], optional): 绑定到 SQL 语句中的参数
                - 若为列表或元组， SQL 中使用 `%s` 占位
                - 若为字典, SQL 中使用 `%(name)s` 占位

                默认为 None

        Returns:
            Any: 单个值或 None
        """
        result = self.query_one(sql, params)
        if result:
            return list(result.values())[0]
        return None
    

    def desc_table(self, table_name: str) -> List[Dict]:
        """查看表结构以及字段注释

        Args:
            table_name (str): 要查看的表名

        Returns:
            Any: _description_
        """
        self.cursor.execute(f'SHOW FULL COLUMNS FROM {table_name}')
        return self.cursor.fetchall()

    
    