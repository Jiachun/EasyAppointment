import os
from dotenv import load_dotenv


# 加载 .env 文件中的环境变量
load_dotenv()


class Config:
    # 通过环境变量获取数据库连接 URI
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

    # 从环境变量加载 Secret Key
    SECRET_KEY = os.getenv('SECRET_KEY')

    # 禁用 SQLAlchemy 对象跟踪修改功能（可选，推荐关闭以节省内存）
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False