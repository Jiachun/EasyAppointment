from .user_views import user_blueprint


def register_blueprints(app):
    app.register_blueprint(user_blueprint, url_prefix='/admin/users')  # 注册用户管理蓝图