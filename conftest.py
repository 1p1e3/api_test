import pytest

from config.settings import settings
from core.api_client import APIClient


@pytest.fixture(scope='session')
def api_client():
    """无认证的通用客户端"""
    return APIClient()


@pytest.fixture(scope='session')
def auth_token():
    """
    登录获取 token
    """
    client = APIClient()
    resp = client.request('POST', f'login', json={
        'username': settings.USERNAME,
        'password': settings.PASSWORD
    })

    token = resp.json()['data']['token']

    return token


