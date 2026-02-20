from pathlib import Path


ROOT_DIR = Path().resolve()

CONFIG_DIR = ROOT_DIR.joinpath('config')

LOGS_DIR = ROOT_DIR.joinpath('logs')

CORE_DIR = ROOT_DIR.joinpath('core')

MODELS_DIR = ROOT_DIR.joinpath('models')

DB_MODELS_DIR = MODELS_DIR.joinpath('db_models')

RESPONSE_MODELS_DIR = MODELS_DIR.joinpath('response_models')

UTILS_DIR = ROOT_DIR.joinpath('utils')

# 测试用例
CASES_DIR = ROOT_DIR.joinpath('cases')

REPORTS_DIR = ROOT_DIR.joinpath('reports')