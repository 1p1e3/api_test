from loguru import logger
from config.paths import LOGS_DIR

LOGS_DIR.mkdir(exist_ok=True)

logger.remove()


