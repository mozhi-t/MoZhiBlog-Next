"""
Database Models - 数据库模型
"""
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, SmallInteger
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from config import config
from logger import logger

# 创建数据库引擎
engine = create_engine(config.DATABASE_URL, echo=False, pool_pre_ping=True)

# 创建会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==================== Models ====================
class Admin(Base):
    __tablename__ = 'admin'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(100), nullable=True)
    create_time = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Admin {self.username}>"


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    create_time = Column(DateTime, default=datetime.now)

    # 关联
    articles = relationship('Article', back_populates='category')

    def __repr__(self):
        return f"<Category {self.name}>"


class Tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    create_time = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Tag {self.name}>"


class Article(Base):
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    summary = Column(String(500), nullable=True)
    content = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=True)
    tags = Column(String(200), nullable=True)  # 标签ID列表
    type = Column(SmallInteger, default=0)  # 文章属性: 0-普通, 1-置顶, 2-密码访问
    access_password = Column(String(255), nullable=True)
    read_count = Column(Integer, default=0)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now)

    category = relationship('Category', back_populates='articles')

    def __repr__(self):
        return f"<Article {self.title}>"


class FriendLink(Base):
    __tablename__ = 'friend_link'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    signature = Column(String(200), nullable=True)
    icon_url = Column(String(500), nullable=True)
    link_url = Column(String(500), nullable=False)
    create_time = Column(DateTime, default=datetime.now)
    is_show = Column(SmallInteger, default=1)
    # 权重字段: 0-挚友, 1-朋友, 2-来客
    weight = Column(SmallInteger, default=2)

    def __repr__(self):
        return f"<FriendLink {self.username}>"


class Blacklist(Base):
    __tablename__ = 'blacklist'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(50), nullable=False, unique=True)
    failed_attempts = Column(Integer, default=0)  # 失败次数
    create_time = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Blacklist {self.ip}>"


# ==================== Create Tables ====================
def create_tables():
    logger.info("开始创建数据库表...")
    Base.metadata.create_all(bind=engine)
    logger.info("数据库表创建成功!")


if __name__ == '__main__':
    create_tables()
