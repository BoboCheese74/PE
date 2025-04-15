from pydantic import BaseModel
from typing import Optional, List


class User(BaseModel):
    """
    用户模型，表示系统中的用户实体。

    属性:
        username: 用户名，唯一标识
        hashed_password: 哈希后的密码
        email: 用户邮箱（可选）
        full_name: 用户全名（可选）
        disabled: 用户是否被禁用，默认为False
        role: 用户角色，默认为"user"，可选值为"user"或"admin"
    """

    username: str
    hashed_password: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = False
    role: str = "user"  # 可选值: "user", "admin"


class UserInDB(User):
    pass


class Token(BaseModel):
    """
    令牌模型，表示授权令牌的响应格式。

    属性:
        access_token: 访问令牌字符串
        token_type: 令牌类型，通常为"bearer"
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    令牌数据模型，表示从令牌中解析出的数据。

    属性:
        username: 用户名（可选）
        role: 用户角色（可选）
    """

    username: Optional[str] = None
    role: Optional[str] = None
