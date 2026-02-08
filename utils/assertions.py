# 两层断言模式：
# 1. 基于 Pydantic 验证数据结构、类型或约束等
# 2. 在 Pydantic 验证通过后，使用传统断言 assert 从功能业务层面验证数据正确性


from requests import Response

from utils.logger import logger


def assert_status_code(response: Response, expected: int, msg=''):
    """断言响应状态码

    Args:
        response (Response): requests 响应对象
        expected (int): 期望值
        msg (str, optional): 功能业务层面的失败信息, 用于说明预期行为, 表现测试和断言意图, 增强断言消息的可读性

        例如: 
        没有额外 msg 说明时, 断言消息为: "响应状态码不匹配, 期望: 400, 实际: 403", 这样的消息不利于阅读, 对团队其他成员可能会造成理解负担。
        如果 msg 的值为 "注册账号已存在时应返回 400", 则完整的断言消息为: "注册账号已存在时应返回 400, 响应状态码不匹配, 期望: 400, 实际: 403"。

        这样的失败消息，具有较好的可读性, 能让维护者快速看懂, 对于日常的维护调试和团队协作是非常好的一种实践。
    """
    actual = response.status_code
    if actual != expected:
        error_msg = f'响应状态码不匹配, 期望: {expected}, 实际: {actual}'
        if msg:
            error_msg += f'{msg} | {error_msg}'
        logger.error(error_msg)