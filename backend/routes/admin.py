"""
Admin Routes - 管理员接口
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from models import Admin, get_db
from schemas import AdminLogin
from auth import verify_password, create_access_token, get_current_admin
from config import config

router = APIRouter(prefix="/api/admin", tags=["管理员"])


@router.post("/login")
def admin_login(admin_data: AdminLogin, db: Session = Depends(get_db)):
    """
    管理员登录
    """
    admin = db.query(Admin).filter(Admin.username == admin_data.username).first()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )

    if not verify_password(admin_data.password, admin.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )

    access_token_expires = timedelta(hours=config.JWT_EXPIRE_HOURS)
    token = create_access_token(
        data={"sub": admin.username},
        expires_delta=access_token_expires
    )

    return {
        "code": 200,
        "msg": "success",
        "data": {
            "token": token,
            "admin": {
                "id": admin.id,
                "username": admin.username,
                "email": admin.email,
                "create_time": admin.create_time.isoformat() if admin.create_time else None
            }
        }
    }


@router.get("/me")
def get_admin_info(admin: Admin = Depends(get_current_admin)):
    """
    获取当前登录管理员信息
    """
    return {
        "code": 200,
        "msg": "success",
        "data": {
            "id": admin.id,
            "username": admin.username,
            "email": admin.email,
            "create_time": admin.create_time.isoformat() if admin.create_time else None
        }
    }


@router.post("/logout")
def admin_logout():
    """
    管理员退出
    """
    return {"code": 200, "msg": "退出成功"}
