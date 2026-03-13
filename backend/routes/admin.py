"""
Admin Routes - 管理员接口
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import timedelta

from models import Admin, Blacklist, get_db
from schemas import AdminLogin, AdminUpdate
from auth import verify_password, create_access_token, get_current_admin, get_password_hash
from config import config
from logger import logger

router = APIRouter(prefix="/api/admin", tags=["管理员"])

MAX_LOGIN_ATTEMPTS = 5  # 最大登录失败次数


@router.post("/login")
def admin_login(request: Request, admin_data: AdminLogin, db: Session = Depends(get_db)):
    # 获取客户端IP
    client_ip = request.client.host
    logger.info(f"管理员登录尝试 - username: {admin_data.username}, ip: {client_ip}")

    # 检查IP是否在黑名单中
    blacklist_entry = db.query(Blacklist).filter(Blacklist.ip == client_ip).first()
    if blacklist_entry:
        logger.warning(f"登录失败 - IP在黑名单中, ip: {client_ip}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您已被拉黑，请联系管理员"
        )

    admin = db.query(Admin).filter(Admin.username == admin_data.username).first()
    if not admin:
        # 用户不存在
        increment_failed_attempts(client_ip, db)
        logger.warning(f"登录失败 - 用户不存在, username: {admin_data.username}, ip: {client_ip}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )

    if not verify_password(admin_data.password, admin.password):
        # 密码错误
        increment_failed_attempts(client_ip, db)
        logger.warning(f"登录失败 - 密码错误, username: {admin_data.username}, ip: {client_ip}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )

    # 登录成功
    if blacklist_entry:
        db.delete(blacklist_entry)
        db.commit()

    logger.info(f"管理员登录成功 - username: {admin.username}, ip: {client_ip}")

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
    blacklist_entry = db.query(Blacklist).filter(Blacklist.ip == ip).first()

    if blacklist_entry:
        blacklist_entry.failed_attempts += 1
        if blacklist_entry.failed_attempts >= MAX_LOGIN_ATTEMPTS:
            # 已达到最大失败次数
            db.commit()
            logger.warning(f"IP已被拉黑 - ip: {ip}, failed_attempts: {blacklist_entry.failed_attempts}")
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
    logger.warning(f"登录失败次数+1 - ip: {ip}, failed_attempts: {blacklist_entry.failed_attempts}")


@router.get("/me")
def get_admin_info(admin: Admin = Depends(get_current_admin)):
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
def admin_logout(request: Request, admin: Admin = Depends(get_current_admin)):
    logger.info(f"管理员退出 - username: {admin.username}")
    return {"code": 200, "msg": "退出成功"}


@router.put("/settings")
def update_admin_settings(
    request: Request,
    settings_data: AdminUpdate,
    admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """修改管理员账户和密码"""
    logger.info(f"管理员尝试修改设置 - username: {admin.username}")

    # 1. 验证当前密码
    if not verify_password(settings_data.current_password, admin.password):
        logger.warning(f"修改设置失败 - 当前密码错误, username: {admin.username}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="当前密码错误"
        )

    # 2. 检查新用户名是否已存在（如果提供了新用户名）
    new_username = settings_data.new_username
    new_password = settings_data.new_password

    if new_username and new_username != admin.username:
        existing_admin = db.query(Admin).filter(Admin.username == new_username).first()
        if existing_admin:
            logger.warning(f"修改设置失败 - 用户名已存在, username: {new_username}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在"
            )
        admin.username = new_username
        logger.info(f"管理员修改用户名 - old: {admin.username}, new: {new_username}")

    # 3. 更新密码（如果提供了新密码）
    if new_password:
        admin.password = get_password_hash(new_password)
        logger.info(f"管理员修改密码 - username: {admin.username}")

    # 4. 保存更改
    db.commit()

    # 5. 重新生成 token（因为用户名可能已更改）
    access_token_expires = timedelta(hours=config.JWT_EXPIRE_HOURS)
    token = create_access_token(
        data={"sub": admin.username},
        expires_delta=access_token_expires
    )

    logger.info(f"管理员设置修改成功 - username: {admin.username}")

    return {
        "code": 200,
        "msg": "设置已更新",
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
