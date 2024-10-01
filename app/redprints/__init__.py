from .user_api import user_api


def register_redprints(app):
    app.register_blueprint(user_api, url_prefix='/api/users')  # 注册用户API