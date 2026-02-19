import json
from typing import Any, Dict, List
from config.paths import CASES_DIR
import yaml

from utils.logger import logger

def load_test_data(file_name: str) -> List[Dict[str, Any]]:
    """
    通用测试数据加载器, 支持 YAML/JSON 格式

    支持文件后缀：.yaml, .yml, .json

    测试用例数据格式:

    ```yaml
    - title: "创建用户 - 成功"
      data:
          username: "heisenberg"
          email: "heisenberg@example.com"
          password: "12345"
      expected:
          status_code: 201
          message: "注册成功"
  
      - title: "创建用户 - 邮箱已存在"
        data:
            username: "gustavo"
            email: "gustavo@example.com"  # 重复邮箱
            password: "12345"
        expected:
            status_code: 400
            error_code: "用户已存在"
    ```

    ```json
    [
        {
            "title": "登录成功",
            "data": {
                "email": "heisenberg@example.com",
                "password": "12345"
            },
            "expected": {
                "status_code": 200,
                "has_token": true
            }
        },
        {
            "title": "登录失败 - 密码错误",
            "data": {
                "email": "heisenberg@example.com",
                "password": "12355"
            },
            "expected": {
                "status_code": 401,
                "error": "账号或密码错误"
            }
        }
    ]
    ```

    Args:
        file_name (str): 数据文件名, 不需要路径

    Returns:
        
        List[Dict[str, Any]]: 解析结果, 每个 dict 代表一条测试用例
    """
    data_file = CASES_DIR.joinpath(file_name)
    if not data_file.exists():
        raise FileNotFoundError(f'测试数据文件不存在: {data_file}')
    
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            if data_file.suffix in ('.yaml', '.yml'):
                data = yaml.safe_load(f)
            elif data_file.suffix == '.json':
                data = json.load(f)
            else:
                raise ValueError(f'不支持的文件格式: {data_file.suffix}. 仅支持 .yaml, .yml, .json')
            
            # 验证数据结构
            if not isinstance(data, list):
                raise ValueError(f'数据根节点必须是列表(list), 当前类型: {type(data).__name__}')
            
            logger.info(f'成功加载测试数据: {data_file} —— {len(data)} 条用例')
            return data
    except yaml.YAMLError as e:
        raise ValueError(f'YAML 文件解析失败 ({data_file}): {e}')
    except json.JSONDecodeError as e:
        raise ValueError(f'JSON 文件解析失败 ({data_file}): {e}')
    except Exception as e:
        raise RuntimeError(f'数据文件加载时出错 ({data_file}): {e}')