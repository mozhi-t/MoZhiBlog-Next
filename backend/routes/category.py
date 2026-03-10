"""
Category Routes - 分类接口
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from models import Category, get_db
from schemas import CategoryCreate, CategoryUpdate
from auth import get_current_admin

router = APIRouter(prefix="/api/categories", tags=["分类"])


@router.get("")
def get_categories(db: Session = Depends(get_db)):
    """
    获取所有分类列表（公开）
    """
    categories = db.query(Category).order_by(Category.create_time.desc()).all()
    return {
        "code": 200,
        "msg": "success",
        "data": [{
            "id": c.id,
            "name": c.name,
            "create_time": c.create_time.isoformat() if c.create_time else None
        } for c in categories]
    }


# ==================== 管理员接口 ====================

@router.post("")
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    """
    新增分类（需管理员鉴权）
    """
    existing = db.query(Category).filter(Category.name == category_data.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="分类名称已存在"
        )

    category = Category(name=category_data.name)
    db.add(category)
    db.commit()
    db.refresh(category)

    return {
        "code": 200,
        "msg": "success",
        "data": {
            "id": category.id,
            "name": category.name,
            "create_time": category.create_time.isoformat() if category.create_time else None
        }
    }


@router.put("/{category_id}")
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    """
    编辑分类（需管理员鉴权）
    """
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="分类不存在"
        )

    if category_data.name and category_data.name != category.name:
        existing = db.query(Category).filter(Category.name == category_data.name).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="分类名称已存在"
            )
        category.name = category_data.name

    db.commit()
    db.refresh(category)

    return {
        "code": 200,
        "msg": "success",
        "data": {
            "id": category.id,
            "name": category.name,
            "create_time": category.create_time.isoformat() if category.create_time else None
        }
    }


@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    """
    删除分类（需管理员鉴权）
    """
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="分类不存在"
        )

    if category.articles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该分类下有文章，无法删除"
        )

    db.delete(category)
    db.commit()

    return {"code": 200, "msg": "删除成功"}
