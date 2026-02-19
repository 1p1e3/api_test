import pytest

from utils.data_loader import load_test_data


def ddt(file_name: str):
    """
    数据驱动装饰器, 配合 pytest 参数化使用

    用法：
        @ddt('test_user.yaml')
        def test_register_user(self, case):
            ...

    Args:
        file_name (str): 数据文件名, 不要路径
    """
    test_cases = load_test_data(file_name)

    # 测试用例 id
    ids = []
    for i, case in enumerate(test_cases):
        # 以测试用例 title 作为 id, 如果为空, 则使用索引作为 id
        case_id = case.get('title') or f'case_{i+1}'
        ids.append(case_id)
    
    return pytest.mark.parametrize(
        argnames='case',
        argvalues=test_cases,
        ids=ids
    )