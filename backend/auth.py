"""
Auth Utils - 认证工具
"""
from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from config import config
from models import Admin, get_db

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Bearer token
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """获取密码哈希"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建JWT Token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=config.JWT_EXPIRE_HOURS)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict:
    """解码JWT Token"""
    try:
        payload = jwt.decode(token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token已过期"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的Token"
        )


async def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Admin:
    """获取当前管理员（鉴权依赖）"""
    token = credentials.credentials

    # 解码token
    payload = decode_token(token)
    username = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的Token载荷"
        )

    # 查询管理员
    admin = db.query(Admin).filter(Admin.username == username).first()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="管理员不存在"
        )

    return admin


async def get_current_admin_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    db: Session = Depends(get_db)
) -> Optional[Admin]:
    """可选的鉴权依赖（不强制要求登录）"""
    if not credentials:
        return None

    try:
        return await get_current_admin(credentials, db)
    except HTTPException:
        return None
