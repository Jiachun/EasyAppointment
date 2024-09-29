from flask import Flask
from config import Config
from extensions.db import init_db


def create_app():
    app = Flask(__name__)

    # 加载配置文件
    app.config.from_object(Config)

    # 初始化数据库
    init_db(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
