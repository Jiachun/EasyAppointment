from .user_api import user_api
from .campus_api import campus_api


def register_redprints(app):
    app.register_blueprint(user_api, url_prefix='/api/users')  # 注册用户API
    app.register_blueprint(campus_api, url_prefix='/api/campuses')  # 注册用户API