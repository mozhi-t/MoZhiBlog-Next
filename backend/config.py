"""
Configuration
"""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')


class Config:
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'root')
    DB_NAME = os.getenv('DB_NAME', 'mozhiblog')

    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key')
    JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
    JWT_EXPIRE_HOURS = int(os.getenv('JWT_EXPIRE_HOURS', 2))

    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173,http://localhost:5174').split(',')
    SITE_URL = os.getenv('SITE_URL', 'https://blog.mozhi.top').rstrip('/')
    API_PORT = int(os.getenv('API_PORT', 8008))

    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_DIR = os.getenv('LOG_DIR', None)
    LOG_BACKUP_COUNT = int(os.getenv('LOG_BACKUP_COUNT', 30))


config = Config()
