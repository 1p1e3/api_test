from contextlib import contextmanager
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from config.settings import settings
from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import sessionmaker, Session

from utils.logger import logger


class MySQLClient:
    """原生 SQL 操作封装
    """

    def __init__(self, 
                 db_url: Optional[str] = None,
                 pool_size: int = 5,
                 max_overflow: int = 10,
                 echo: bool = False,
                 ):
        # 如果手动传了 db_url 则用手动传的；反之就读环境变量配置的
        self.db_url = db_url or settings.MYSQL_DB_URL

        # 
        self.engine: Engine = create_engine(
            self.db_url,
            poolclass=QueuePool,
            pool_size=pool_size or settings.MYSQL_POOL_SIZE,
            max_overflow=max_overflow or settings.MYSQL_MAX_OVERFLOW,
            pool_pre_ping=True,     # 每次取连接时 ping 一下，避免 stale connection
            echo=echo or (False if settings.APP_ENV == 'prod' else True)
        )

        self.SessionLocal = sessionmaker(bind=self.engine)

        logger.info(f'{settings.APP_ENV} 环境 MySQLClient 初始化成功')
    

    def get_session(self) -> Session:
        return self.SessionLocal()
    

    @contextmanager
    def get_auto_session(self):
        session = self.SessionLocal()

        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f'MySQL 事务失败: {e}')
            raise
        finally:
            session.close()
    

    