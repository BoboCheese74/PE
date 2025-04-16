from main import Main
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from datetime import timedelta
from models import LoginResponse, User
from security import (
    authenticate_user,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_active_user,
    fake_users_db,
    get_password_hash,
    check_admin_permission,
)
from typing import List

# 创建 FastAPI 应用实例
app = FastAPI()

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 允许所有源，也可以指定特定源，如 ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)

Main = Main()

# current_user: User = Depends(get_current_active_user)


# 登录接口，获取token
@app.post("/token", response_model=LoginResponse)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    用户登录接口，接收用户名和密码并返回访问令牌。

    参数:
        form_data: OAuth2标准表单，包含username和password字段

    返回:
        Token对象: 包含access_token和token_type

    异常:
        401 Unauthorized: 如果用户名或密码错误
    """
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        return {
            "code": 2001,
            "message": "访问失败",
            "succeed": False,
            "access_token": "",  # 提供空字符串作为默认值
            "token_type": "bearer",
            "data": {"username": ""},
        }
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
    )
    return {
        "code": 200,
        "message": "访问成功",
        "succeed": True,
        "access_token": access_token,
        "token_type": "bearer",
        "data": {"username": user.username},
    }


# 注册接口
@app.post("/register")
async def register_user(username: str, password: str, email: str = None, full_name: str = None, role: str = "user"):
    """
    用户注册接口，创建新用户并添加到用户数据库中。

    参数:
        username: 用户名（必填）
        password: 密码（必填）
        email: 电子邮箱（可选）
        full_name: 全名（可选）
        role: 用户角色，默认为"user"

    返回:
        成功消息对象

    异常:
        400 Bad Request: 如果用户名已存在
    """
    if username in fake_users_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在")
    hashed_password = get_password_hash(password)
    fake_users_db[username] = {
        "username": username,
        "hashed_password": hashed_password,
        "email": email,
        "full_name": full_name,
        "disabled": False,
        "role": role,
    }
    return {"message": "用户注册成功"}


# 获取当前用户信息
@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    获取当前已认证用户的信息。

    依赖:
        current_user: 当前已认证且处于活跃状态的用户

    返回:
        User对象: 当前用户的完整信息（不包含密码哈希）

    说明:
        此接口需要有效的Bearer令牌才能访问
    """
    print(type(current_user))
    return current_user


# 添加权限验证到现有接口
@app.get("/generate_outline")
async def generate_outline(
    language: str, title: str, LLM: str = "openai", current_user: User = Depends(get_current_active_user)
):
    """
    通过gpt生成提纲内容（promt）
    :param language: str 语言类型 只有中文和英文 除了中文以外的输入都默认为英文
    :param title: str 文章标题
    :param LLM: str 使用的大语言模型名称
    """
    response = Main.generate_outline(language, title, LLM)
    return {
        "code": 200,
        "message": "访问成功",
        "succeed": True,
        "data": {"outline": response},
    }


@app.get("/get_keyword")
async def get_keyword(content: str, LLM: str = "deepseek", current_user: User = Depends(get_current_active_user)):
    """
    通过提纲提取关键词（用deepseek）
    :param content: str 提纲内容 是generate_outline()的返回值
    :param LLM: str 使用的大语言模型名称
    """
    response = Main.get_keyword(content, LLM)
    return {"code": 200, "message": "访问成功", "succeed": True, "data": {"keywords": response}}


@app.get("/search_pubmed")
async def search_pubmed(
    keywords, max_per_keyword: int = 5, max_total: int = 30, current_user: User = Depends(get_current_active_user)
):
    """
    根据关键词去pubmed检索文献（近10年，影响因子>0.001，每个关键词最多5篇，一共不超过30篇）
    :param keywords: list 关键词列表 是get_keyword()的返回值
    :param max_per_keyword: int 每个关键词最多返回的文献数量
    :param max_total: int 总共返回的文献数量
    """
    response = Main.search_pubmed(keywords, max_per_keyword, max_total)
    return {
        "code": 200,
        "message": "访问成功",
        "succeed": True,
        "data": {"keywords": keywords, "max_per_keyword": max_per_keyword, "max_total": max_total, "papers": response},
    }


@app.get("/edit")
async def edit(
    language: str,
    title: str,
    prompt_outline: str,
    paper: str,
    LLM: str = "anthropic",
    current_user: User = Depends(get_current_active_user),
):
    """
    Claude生成文章
    :param language: str 语言类型 只有中文和英文 除了中文以外的输入都默认为英文
    :param title: str 文章标题
    :param prompt_outline: str 提纲内容 generate_outline()的返回值
    :param paper: str 文献内容 search_pubmed()的返回值
    :param LLM: str 使用的大语言模型名称
    """
    print(language, title, prompt_outline, paper, LLM)

    response = Main.edit(language, title, prompt_outline, paper, LLM)

    return {
        "code": 200,
        "message": "访问成功",
        "succeed": True,
        "data": {
            "language": language,
            "title": title,
            "prompt_outline": prompt_outline,
            "paper": paper,
            "LLM": LLM,
            "paper_content": response,
        },
    }


# 管理员接口示例 - 查看所有用户
@app.get("/admin/users", response_model=List[User])
async def get_all_users(current_user: User = Depends(check_admin_permission)):
    """
    管理员接口：获取所有用户的信息列表。

    依赖:
        current_user: 通过管理员权限检查的用户

    返回:
        User对象列表: 系统中所有用户的信息

    权限:
        仅限管理员角色访问

    异常:
        403 Forbidden: 如果当前用户不是管理员
    """
    return [User(**user_data) for user_data in fake_users_db.values()]
