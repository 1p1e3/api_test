from pydantic import BaseModel

# 示例数据表模型

class DBUserModel(BaseModel):
    id: int
    name: str
    