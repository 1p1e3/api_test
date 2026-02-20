from core.ddt import ddt
import responses

from models.response_models.user_model import CreateUserModel
from utils.assertions import assert_response_model, assert_status_code


@responses.activate
@ddt('test_user.yaml')
def test_create_user(unauthorized_client, case):
    """测试用例 - 创建用户
    """
    expected = case['expected']
    expected_status = expected['status_code']
    
    mock_json = {
        'code': 200 if expected_status == 201 else 400,
        'message': expected.get('message', '注册成功') if expected_status == 201 else expected.get('error_code'),
        'data': {'id': 1} if expected_status == 201 else None
    }

    responses.add(
        responses.POST, 
        'http://127.0.0.1/register',
        json=mock_json,
        status=expected_status
        )
    
    # 测试用例请求执行
    resp = unauthorized_client.post('/register', json=case['data'])
    assert_status_code(resp, case['expected']['status_code'], msg=case.get('title'))
    if expected_status == 201:
        model = assert_response_model(resp, CreateUserModel)
        assert model.data.id == 1