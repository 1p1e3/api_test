import pytest

from config.settings import settings
from core.api_client import APIClient


@pytest.fixture(scope='session')
def api_client():
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


