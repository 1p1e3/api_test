from pydantic_settings import BaseSettings
from typing import Literal
from pydantic import Field, field_validator
import os

Environment = Literal['dev', 'test', 'prod']

class Settings(BaseSettings):
    APP_ENV: Environment = Field(default='test')

    API_BASE_URL: str

    USERNAME: str

    PASSWORD: str


    def __init__(self, **data):
        env = os.getenv('APP_ENV', 'test').lower()
        env_file = f'.env.{env}'

        if not os.path.exists(env_file):
            print(f'{env_file} 未找到')
            env_file = None
        
        super().__init__(_env_file=env_file, **data)
    

    @field_validator
    @classmethod
    def validate_api_base_url(cls, v) -> str:
        if not isinstance(v, str):
            raise TypeError('API_BASE_URL 必须为 str 类型')

        v = v.strip()

        if not v.startswith(('http://', 'https://')):
            raise ValueError('API_BASE_URL 必须以 "http://" 或 "https://" 开头')

        return v.rstrip('/')
    

    model_config = {
        'extra': 'ignore',
        'env_file_encoding': 'utf-8'
    }
    

# 单例
settings = Settings()