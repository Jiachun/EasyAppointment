from flask_sqlalchemy import SQLAlchemy


# 实例化 SQLAlchemy 对象
db = SQLAlchemy()


def init_db(app):
    """
    初始化数据库，将数据库与 Flask 应用关联。
    """
    db.init_app(app)