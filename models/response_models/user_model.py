from typing import Any
from pydantic import BaseModel

# 示例接口响应模型
class CreateUserData(BaseModel):
    id: int

class CreateUserModel(BaseModel):
    code: int
    message: str
    data: CreateUserData