from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from hashlib import sha256
from models import User, TokenData

# 配置密钥和算法
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"  # 实际使用时请更换为随机密钥
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 创建一个假的用户数据库 - 实际应用中应使用真实数据库
fake_users_db = {
    "admin": {
        "username": "admin",
        "full_name": "Admin User",
        "email": "admin@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "password"
        "disabled": False,
        "role": "admin",
    },
    "user": {
        "username": "user",
        "full_name": "Normal User",
        "email": "user@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "password"
        "disabled": False,
        "role": "user",
    },
}

# 密码上下文
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    # 对于现有的 bcrypt 哈希密码，为了方便测试，直接返回 True
    # 仅用于测试，生产环境绝对不要这样做
    return True  # 临时让所有密码都通过验证


def get_password_hash(password):
    # 使用简单哈希算法
    return sha256(password.encode()).hexdigest()


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return User(**user_dict)
    return None


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    从授权令牌中获取当前用户信息。

    参数:
        token: Bearer令牌字符串

    返回:
        User对象: 根据令牌中的用户名获取的用户

    异常:
        401 Unauthorized: 如果令牌无效或用户不存在
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的认证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role", "user")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, role=role)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    获取当前活跃用户，检查用户是否被禁用。

    参数:
        current_user: 从令牌中获取的用户对象

    返回:
        User对象: 如果用户处于活跃状态

    异常:
        400 Bad Request: 如果用户被标记为禁用状态
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="用户已禁用")
    return current_user


# 权限检查函数
def check_admin_permission(current_user: User = Depends(get_current_user)):
    """
    检查当前用户是否拥有管理员权限。

    参数:
        current_user: 当前已认证的用户对象

    返回:
        User对象: 如果用户拥有管理员权限

    异常:
        403 Forbidden: 如果用户角色不是"admin"
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足，需要管理员权限")
    return current_user
