import os

from flask import Flask
from flask_cors import CORS

from app.config import DevelopmentConfig, ProductionConfig
from app.redprints import register_redprints
from extensions.db import init_db, init_redis


def create_app():
    app = Flask(__name__)

    # 允许所有跨域请求 
    # TODO 安全设置
    CORS(app)

    # 根据环境变量加载配置
    if os.getenv('FLASK_ENV') == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # 初始化数据库
    init_db(app)

    # 初始化 Redis
    init_redis(app)

    # 注册红图
    register_redprints(app)

    return app
