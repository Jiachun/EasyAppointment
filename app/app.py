import os
from flask import Flask
from app.config import DevelopmentConfig, ProductionConfig
from extensions.db import init_db
from app.redprints import register_redprints
from app.blueprints import register_blueprints


def create_app():
    app = Flask(__name__)

    # 根据环境变量加载配置
    if os.getenv('FLASK_ENV') == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # 初始化数据库
    init_db(app)

    # 注册蓝图和红图
    register_redprints(app)
    register_blueprints(app)

    return app
