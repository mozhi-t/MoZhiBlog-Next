# Blog Backend - Python FastAPI

## 环境要求
- Python 3.8+
- MySQL 5.7+/8.0

## 安装依赖
```bash
cd backend
pip install -r requirements.txt
```

## 配置说明
1. 复制 `.env.example` 为 `.env`
2. 修改 `.env` 中的数据库配置和JWT密钥

## 数据库初始化
```bash
python init_db.py
```

## 启动服务
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 接口文档
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 测试账号
- 用户名: admin
- 密码: 123456
