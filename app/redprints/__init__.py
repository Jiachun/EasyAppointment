from .user_api import user_api
from .campus_api import campus_api
from .role_api import role_api
from .permission_api import permission_api


def register_redprints(app):
    app.register_blueprint(user_api, url_prefix='/api/users')  # 注册用户管理API
    app.register_blueprint(campus_api, url_prefix='/api/campuses')  # 注册校区管理API
    app.register_blueprint(role_api, url_prefix='/api/roles')  # 注册角色管理API
    app.register_blueprint(permission_api, url_prefix='/api/permissions')  # 注册权限管理API