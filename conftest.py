import pytest

from config.settings import settings
from core.api_client import APIClient
from core.mysql_client import MySQLClient


@pytest.fixture(scope='session')
def unauthorized_client():
    """无认证的通用客户端"""
    return APIClient()


@pytest.fixture(scope='session')
def authorized_client(api_client):
    """
    带认证的通用客户端
    """
    resp = api_client.request('POST', f'login', json={
        'username': settings.USERNAME,
        'password': settings.PASSWORD
    })
    assert resp.status_code == 200

    token = resp.json()['data']['token']

    assert token, '创建带认证的客户端失败, 未获取到 token'

    api_client.set_token(token)

    return api_client



# 利用 pytest 的 fixture 特性，实现数据库连接的获取
# 利用 pytest 生命周期钩子函数，实现数据库连接池的关闭
@pytest.fixture(scope='function')
def db():
    """函数级别的 fixture, 每个测试用例获取一个独立的数据库连接
    """
    with MySQLClient() as client:
        yield client

def pytest_sessionfinish(session, exitstatus):
    """测试结束后操作
    """
    # 关闭 MySQL 连接池
    MySQLClient.close_pool()

