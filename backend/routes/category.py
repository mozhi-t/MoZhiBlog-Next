"""
Category routes.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth import get_current_admin
from cache import cache
from logger import logger
from models import Category, get_db
from schemas import CategoryCreate, CategoryUpdate

router = APIRouter(prefix="/api/categories", tags=["categories"])

CATEGORIES_CACHE_KEY = "categories:list"


def invalidate_category_cache():
    cache.delete(CATEGORIES_CACHE_KEY)


@router.get("")
def get_categories(db: Session = Depends(get_db)):
    def load_categories():
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

    return cache.get_or_set(CATEGORIES_CACHE_KEY, load_categories)


@router.post("")
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    existing = db.query(Category).filter(Category.name == category_data.name).first()
    if existing:
        logger.warning(f"category name already exists - name: {category_data.name}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category name already exists.",
        )

    category = Category(name=category_data.name)
    db.add(category)
    db.commit()
    db.refresh(category)
    invalidate_category_cache()

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
    logger.info(f"category updated - category_id: {category_id}, author: {admin.username}")

    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        logger.warning(f"category not found - category_id: {category_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category does not exist.",
        )

    if category_data.name and category_data.name != category.name:
        existing = db.query(Category).filter(Category.name == category_data.name).first()
        if existing:
            logger.warning(f"category name already exists - name: {category_data.name}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category name already exists.",
            )
        category.name = category_data.name

    db.commit()
    db.refresh(category)
    invalidate_category_cache()

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
    logger.info(f"category deleted - category_id: {category_id}, author: {admin.username}")

    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        logger.warning(f"category not found - category_id: {category_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category does not exist.",
        )

    if category.articles:
        logger.warning(f"category has articles and cannot be deleted - category_id: {category_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category has articles and cannot be deleted.",
        )

    db.delete(category)
    db.commit()
    invalidate_category_cache()

    return {"code": 200, "msg": "Delete successful."}
