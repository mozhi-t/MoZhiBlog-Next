"""
Configuration - 应用配置
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')


class Config:
    """应用配置类"""

    # 数据库配置
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'root')
    DB_NAME = os.getenv('DB_NAME', 'mozhiblog')

    # 数据库连接URL
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # JWT配置
    JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key')
    JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
    JWT_EXPIRE_HOURS = int(os.getenv('JWT_EXPIRE_HOURS', 2))

    # CORS配置
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173,http://localhost:5174').split(',')


config = Config()
