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
    encoding='utf-8',
    enqueue=True,
    format='{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}'
)


# 标准输出
_logger.add(
    sink=sys.stdout,
    level='DEBUG',
    colorize=True,
    format='<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | {level: <8} | {name}:{function}:{line} - {message}'
)


# 标准错误
_logger.add(
    sink=sys.stderr,
    level='ERROR',
    colorize=True,
    format='<red>{time:YYYY-MM-DD HH:mm:ss.SSS}</red> | {level: <8} | {name}:{function}:{line} - {message}'
)


# 单例
logger = _logger



