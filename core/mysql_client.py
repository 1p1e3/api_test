from typing import Optional, cast
from dbutils.pooled_db import PooledDB
from pymysql.cursors import DictCursor

from config.settings import settings

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
                creator=DictCursor,
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
    