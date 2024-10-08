from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis


# 实例化 SQLAlchemy 对象
db = SQLAlchemy()

# 实例化 FlaskRedis 对象
redis_client = FlaskRedis()


def init_db(app):
    """
    初始化数据库，将数据库与 Flask 应用关联。
    """
    db.init_app(app)

def init_redis(app):
    """
    初始化 Redis ，将 Redis 与 Flask 应用关联。
    """
    redis_client.init_app(app)