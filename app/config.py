import os
import redis
from dotenv import load_dotenv


# 加载 .env 文件中的环境变量
load_dotenv()


class Config:
    # 通过环境变量获取数据库连接 URI
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

    # 从环境变量加载 Secret Key
    SECRET_KEY = os.getenv('SECRET_KEY')

    # 从环境变量加载 JWT Secret Key
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

    # 从环境变量加载 Token Expiry
    TOKEN_EXPIRY = os.getenv('TOKEN_EXPIRY')

    # 从环境变量加载 Token 强制刷新的阈值
    REFRESH_THRESHOLD = os.getenv('REFRESH_THRESHOLD')

    # 从环境变量加载多次登录失败锁定时间
    LOCK_TIME = os.getenv('LOCK_TIME')

    # 从环境变量加载最大登录尝试次数
    MAX_LOGIN_ATTEMPTS = os.getenv('MAX_LOGIN_ATTEMPTS')

    # 从环境变量中加载 Redis URL
    SESSION_REDIS = redis.from_url(os.getenv('REDIS_URL'))

    # 从环境变量中加载 AppID
    WECHAT_APP_ID = os.getenv('WECHAT_APP_ID')

    # 从环境变量中加载 AppSecret
    WECHAT_APP_SECRET = os.getenv('WECHAT_APP_SECRET')

    # 从环境变量中加载 PUBLIC KEY
    PUBLIC_KEY = os.getenv('PUBLIC_KEY')

    # 从环境变量中加载 PRIVATE KEY
    PRIVATE_KEY = os.getenv('PRIVATE_KEY')

    # 从环境变量中加载公钥文件路径
    PUBLIC_KEY_PATH = os.getenv('PUBLIC_KEY_PATH')

    # 从环境变量中加载私钥文件路径
    PRIVATE_KEY_PATH = os.getenv('PRIVATE_KEY_PATH')

    # 禁用 SQLAlchemy 对象跟踪修改功能（可选，推荐关闭以节省内存）
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False