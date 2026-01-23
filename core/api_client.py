from typing import Dict, Optional
from requests import Session
from config.settings import settings
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

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
    




        

