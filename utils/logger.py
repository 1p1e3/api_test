from loguru import logger as _logger
from config.paths import LOGS_DIR
import sys

LOGS_DIR.mkdir(exist_ok=True)

_logger.remove()


# 输出到文件
_logger.add(
    sink=LOGS_DIR.joinpath('app.logs'),
    level='INFO',
    rotation='1 day',
    retention='7 days',
    compression='zip',
    enqueue=True,
    format='{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}'
)


# 标准输出
_logger.add(
    sink=sys.stdout,
    level='DEBUG',
    colorize=True,
    format='<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | {name}:{function}:{line} - {message}'
)


# 单例
logger = _logger



