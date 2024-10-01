from .admin import user_blueprint
from .admin import campus_blueprint


def register_blueprints(app):
    app.register_blueprint(user_blueprint, url_prefix='/admin/users')  # 注册用户管理蓝图
    app.register_blueprint(campus_blueprint, url_prefix='/admin/campuses')  # 注册校区管理蓝图