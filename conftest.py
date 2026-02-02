import pytest

from core.api_client import APIClient


@pytest.fixture(scope='session')
def api_client():
    """无认证的通用客户端"""
    return APIClient()



