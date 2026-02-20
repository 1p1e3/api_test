import pytest

from config.settings import Settings
from core.api_client import APIClient
from core.mysql_client import MySQLClient
from utils.notifier import Notifier

settings = Settings()

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


def pytest_collection_modifyitems(items):
    # 测试用例 ID 字符转义处理
    for item in items:  
        item.name = item.name.encode("utf-8").decode("unicode-escape")  
        item._nodeid = item._nodeid.encode("utf-8").decode("unicode-escape")


def pytest_addoption(parser):
    """注册自定义命令行选项"""
    parser.addoption(
        '--report-path',
        action='store',
        default='',
        help='HTML 报告的实际路径（用于通知推送）'
    )


@pytest.hookimpl(trylast=True)
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """
    pytest 执行结束后自动触发
    - 收集测试统计
    - 发送通知
    """
    # 获取统计信息
    stats = terminalreporter.stats
    total = sum(len(stats.get(key, [])) for key in ['passed', 'failed', 'error', 'skipped'])

    summary = {
        'total': total,
        'passed': len(stats.get('passed', [])),
        'failed': len(stats.get('failed', [])),
        'error': len(stats.get('error', [])),
        'skipped': len(stats.get('skipped', [])),
    }

    # 从 config 中获取动态报告路径
    report_path = config.getoption("--report-path")

    # 发送通知
    notifier = Notifier()
    notifier.send_report(summary, report_path=report_path)