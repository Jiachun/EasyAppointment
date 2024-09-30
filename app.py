from flask import Flask
from config import DevelopmentConfig
from extensions.db import init_db


def create_app():
    app = Flask(__name__)

    # 加载配置文件
    app.config.from_object(DevelopmentConfig)

    # 初始化数据库
    init_db(app)

    return app
