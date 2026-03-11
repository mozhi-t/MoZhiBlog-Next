"""
Admin Routes - 管理员接口
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import timedelta

from models import Admin, Blacklist, get_db
from schemas import AdminLogin
from auth import verify_password, create_access_token, get_current_admin
from config import config

router = APIRouter(prefix="/api/admin", tags=["管理员"])

MAX_LOGIN_ATTEMPTS = 5  # 最大登录失败次数


@router.post("/login")
def admin_login(request: Request, admin_data: AdminLogin, db: Session = Depends(get_db)):
    """
    管理员登录
    """
    # 获取客户端IP
    client_ip = request.client.host

    # 检查IP是否在黑名单中
    blacklist_entry = db.query(Blacklist).filter(Blacklist.ip == client_ip).first()
    if blacklist_entry:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您已被拉黑，请联系管理员"
        )

    admin = db.query(Admin).filter(Admin.username == admin_data.username).first()
    if not admin:
        # 用户不存在，增加错误计数
        increment_failed_attempts(client_ip, db)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )

    if not verify_password(admin_data.password, admin.password):
        # 密码错误，增加错误计数
        increment_failed_attempts(client_ip, db)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )

    # 登录成功，重置错误计数
    if blacklist_entry:
        db.delete(blacklist_entry)
        db.commit()

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


def increment_failed_attempts(ip: str, db: Session):
    """增加登录失败次数，达到5次则拉黑IP"""
    blacklist_entry = db.query(Blacklist).filter(Blacklist.ip == ip).first()

    if blacklist_entry:
        blacklist_entry.failed_attempts += 1
        if blacklist_entry.failed_attempts >= MAX_LOGIN_ATTEMPTS:
            # 已达到最大失败次数，不做额外操作，只是阻止登录
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="您已被拉黑，请联系管理员"
            )
    else:
        blacklist_entry = Blacklist(
            ip=ip,
            failed_attempts=1
        )
        db.add(blacklist_entry)

    db.commit()


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
