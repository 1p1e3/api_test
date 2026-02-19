# 两层断言模式：
# 1. 基于 Pydantic 验证数据结构、类型或约束等
# 2. 在 Pydantic 验证通过后，使用传统断言 assert 从功能业务层面验证数据正确性


import json

from requests import Response

from utils.logger import logger

from pydantic import BaseModel, ValidationError

from typing import Type


def assert_status_code(resp: Response, expected: int, msg=''):
    """断言响应状态码

    Args:
        resp (Response): requests 响应结果
        expected (int): 期望值
        msg (str, optional): 功能业务层面的失败信息, 用于说明预期行为, 表现测试和断言意图, 增强断言消息的可读性

        例如: 
        没有额外 msg 说明时, 断言消息为: "响应状态码不匹配, 期望: 400, 实际: 403", 这样的消息不利于阅读, 对团队其他成员可能会造成理解负担。
        如果 msg 的值为 "注册账号已存在时应返回 400", 这样的失败消息，具有较好的可读性, 能让维护者快速看懂, 对于日常的维护调试和团队协作是非常好的一种实践。
    """
    actual = resp.status_code
    if actual != expected:
        error_msg = msg or f'响应状态码不匹配, 期望: {expected}, 实际: {actual}'
        logger.error(error_msg)
        raise AssertionError(error_msg)
    logger.success(f'状态码断言通过: {actual}')


def assert_response_model(resp: Response, model: Type[BaseModel], msg='') -> BaseModel:
    """基于 Pydantic 模型断言整个响应体

    Args:
        resp (Response): requests 响应结果
        model (Type[BaseModel]): 用于断言的响应模型
        msg (str, optional): 功能业务层面的失败信息, 用于说明预期行为, 表现测试和断言意图, 增强断言消息的可读性

    Returns:
        BaseModel: 解析通过后的响应模型实例, 解析通过之后, 就可以对单个字段进行属性访问形式的调用, 对单个字段的断言非常方便
    
    Example:
        class UserResponse(BaseModel):
            id: int
            name: str
            email: str

        assert_response_model(resp, UserResponse)
    """
    try:
        data = resp.json()
        # 自动验证并解析为模型实例
        parsed = model.model_validate(data)
        logger.success(f'Pydantic 模型断言通过: {model.__name__}')
        return parsed
    except ValidationError as e:
        error_msg = msg or f'响应不符合 {model.__name__} 模型:\n{e}'
        logger.error(f'Pydantic 断言失败: {error_msg}')
        raise AssertionError(error_msg)
    except json.JSONDecodeError:
        logger.error('响应不是有效的 JSON')


    