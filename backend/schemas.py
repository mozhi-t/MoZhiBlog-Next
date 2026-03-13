"""
Schemas - Pydantic模型定义
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


# ==================== 通用响应 ====================

class Response(BaseModel):
    """统一响应格式"""
    code: int = 200
    msg: str = "success"
    data: Optional[dict | list] = None


# ==================== 管理员 ====================

class AdminLogin(BaseModel):
    """管理员登录请求"""
    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=1)


class AdminResponse(BaseModel):
    """管理员信息响应"""
    id: int
    username: str
    email: Optional[str] = None
    create_time: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Token响应"""
    token: str
    admin: AdminResponse


class AdminUpdate(BaseModel):
    """修改管理员信息请求"""
    current_password: str = Field(..., min_length=1, description="当前密码")
    new_username: Optional[str] = Field(None, min_length=1, max_length=50, description="新用户名，不修改则为空")
    new_password: Optional[str] = Field(None, min_length=1, description="新密码，不修改则为空")


class AdminUpdateResponse(BaseModel):
    """修改管理员信息响应"""
    token: Optional[str] = None
    admin: AdminResponse


# ==================== 文章 ====================

class ArticleCreate(BaseModel):
    """创建文章请求"""
    title: str = Field(..., min_length=1, max_length=200)
    summary: Optional[str] = Field(None, max_length=500)
    content: str = Field(..., min_length=1)
    category_id: Optional[int] = None
    tags: Optional[str] = Field(None, description="标签ID列表，用逗号分隔，如 '1,2,3'")
    type: int = Field(0, description="文章类型: 0-文章, 1-说说")


class ArticleUpdate(BaseModel):
    """更新文章请求"""
    title: Optional[str] = Field(None, max_length=200)
    summary: Optional[str] = Field(None, max_length=500)
    content: Optional[str] = None
    category_id: Optional[int] = None
    tags: Optional[str] = Field(None, description="标签ID列表，用逗号分隔，如 '1,2,3'")
    type: Optional[int] = Field(None, description="文章类型: 0-文章, 1-说说")


class ArticleListResponse(BaseModel):
    """文章列表响应"""
    id: int
    title: str
    summary: Optional[str] = None
    category_id: Optional[int] = None
    tags: Optional[str] = None
    type: int = 0
    read_count: int
    create_time: datetime
    update_time: datetime
    category: Optional['CategorySimple'] = None
    tag_list: Optional[List['TagSimple']] = None

    class Config:
        from_attributes = True


class ArticleDetailResponse(BaseModel):
    """文章详情响应"""
    id: int
    title: str
    summary: Optional[str] = None
    content: str
    category_id: Optional[int] = None
    tags: Optional[str] = None
    type: int = 0
    read_count: int
    create_time: datetime
    update_time: datetime
    category: Optional['CategorySimple'] = None
    tag_list: Optional[List['TagSimple']] = None

    class Config:
        from_attributes = True


# ==================== 分类 ====================

class CategoryCreate(BaseModel):
    """创建分类请求"""
    name: str = Field(..., min_length=1, max_length=50)


class CategoryUpdate(BaseModel):
    """更新分类请求"""
    name: Optional[str] = Field(None, min_length=1, max_length=50)


class CategoryResponse(BaseModel):
    """分类响应"""
    id: int
    name: str
    create_time: datetime

    class Config:
        from_attributes = True


class CategorySimple(BaseModel):
    """简单分类（用于嵌套）"""
    id: int
    name: str

    class Config:
        from_attributes = True


# ==================== 标签 ====================

class TagSimple(BaseModel):
    """简单标签（用于嵌套）"""
    id: int
    name: str

    class Config:
        from_attributes = True


class TagCreate(BaseModel):
    """创建标签请求"""
    name: str = Field(..., min_length=1, max_length=50)


class TagUpdate(BaseModel):
    """更新标签请求"""
    name: Optional[str] = Field(None, min_length=1, max_length=50)


class TagResponse(BaseModel):
    """标签响应"""
    id: int
    name: str
    create_time: datetime
    article_count: Optional[int] = 0

    class Config:
        from_attributes = True


# ==================== 友链 ====================

class FriendLinkCreate(BaseModel):
    """创建友链请求"""
    username: str = Field(..., min_length=1, max_length=50)
    signature: Optional[str] = Field(None, max_length=200)
    icon_url: Optional[str] = Field(None, max_length=500)
    link_url: str = Field(..., max_length=500)
    weight: Optional[int] = Field(2, description="权重: 0-挚友, 1-朋友, 2-来客")


class FriendLinkUpdate(BaseModel):
    """更新友链请求"""
    username: Optional[str] = Field(None, min_length=1, max_length=50)
    signature: Optional[str] = Field(None, max_length=200)
    icon_url: Optional[str] = Field(None, max_length=500)
    link_url: Optional[str] = Field(None, max_length=500)
    is_show: Optional[int] = None
    weight: Optional[int] = Field(None, description="权重: 0-挚友, 1-朋友, 2-来客")


class FriendLinkResponse(BaseModel):
    """友链响应"""
    id: int
    username: str
    signature: Optional[str] = None
    icon_url: Optional[str] = None
    link_url: str
    create_time: datetime
    is_show: int
    weight: int = 2

    class Config:
        from_attributes = True


# ==================== 分页 ====================

class PaginatedResponse(BaseModel):
    """分页响应"""
    items: List
    total: int
    page: int
    size: int
    pages: int
