from typing import Any, Dict, Optional, Union
from requests import Session
from config.settings import settings
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import requests

from utils.logger import logger

class APIClient:
    def __init__(self,
                 base_url: Optional[str] = None,
                 extra_header: Optional[Dict[str, str]] = None,
                 timeout: int = 10,
                 max_retries: int = 3,
                 ):
        
        # 优先使用实例化时显式传入的 base_url
        self.base_url = base_url or settings.API_BASE_URL
        
        # 
        self.session = Session()
        # 设置请求 header
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
            **(extra_header or {})
        })

        self.timeout = timeout


        # 重试策略
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=['HEAD', 'GET', 'OPTIONS', 'POST', 'PUT', 'DELETE']
        )


        # 配置适配器
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)


        # token
        self.token: Optional[str] = None



    def set_token(self, token: str) -> None:
        """为请求头添加 token

        Args:
            token (_type_): 默认 Bearer Token
        """
        self.token = token
        self.session.headers.update({
            'Authorization': f'Bearer {token}'
        })

    
    def clear_token(self) -> None:
        """清除 token
        """
        self.token = None
        self.session.headers.pop('Authorization', None)
    

    def request(self, 
                method: str,
                api: str,
                *,
                params: Optional[Dict[str, Any]] = None,
                data: Optional[Union[Dict[str, Any], str]] = None,
                json: Optional[Dict[str, Any]] = None,
                headers: Optional[Dict[str, str]] = None,
                timeout: Optional[int] = None,
                **kwargs,
                ) -> requests.Response:
        full_url = self.base_url.rstrip('/') + '/' + api.lstrip('/')

        print(full_url)
        
        # 处理请求数据
        req_kwargs = {
            'params': params,
            'data': data,
            'json': json,
            'headers': headers,
            'timeout': timeout or self.timeout,
            **kwargs,
        }
        # 移除 None 值
        req_kwargs = {k : v for k, v in req_kwargs.items() if v is not None }

        # 发送请求
        try:
            response = self.session.request(method=method, url=full_url, **kwargs)
        except Exception as e:
            logger.error(f'通用请求失败: {e}')
            raise e

 
        return response
    
    
    # 快捷请求方法
    def get(self, api: str, **kwargs) -> requests.Response:
        try:
            response = self.session.request('GET', api, **kwargs)
            return response
        except Exception as e:
            logger.error(f'GET 请求失败: {e}')


    def post(self, api: str, **kwargs) -> requests.Response:
        try:
            response = self.session.request('POST', api, **kwargs)
            return response
        except Exception as e:
            logger.error(f'POST 请求失败: {e}')
    

    def put(self, api: str, **kwargs) -> requests.Response:
        try:
            response = self.session.request('PUT', api, **kwargs)
            return response
        except Exception as e:
            logger.error(f'PUT 请求失败: {e}')
    

    def delete(self, api: str, **kwargs) -> requests.Response:
        try:
            response = self.session.request('DELETE', api, **kwargs)
            return response
        except Exception as e:
            logger.error(f'DELETE 请求失败: {e}')
    

    def patch(self, api: str, **kwargs) -> requests.Response:
        try:
            response = self.session.request('PATCH', api, **kwargs)
            return response
        except Exception as e:
            logger.error(f'PATCH 请求失败: {e}')
    

    def options(self, api: str, **kwargs) -> requests.Response:
        try:
            response = self.session.request('OPTIONS', api, **kwargs)
            return response
        except Exception as e:
            logger.error(f'OPTIONS 请求失败: {e}')
