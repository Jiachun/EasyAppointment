from .user_api import user_api
from .role_api import role_api
from .permission_api import permission_api
from .user_role_api import user_role_api
from .role_permission_api import role_permission_api
from .department_api import department_api
from .user_department_api import user_department_api
from .campus_api import campus_api
from .visitor_api import visitor_api
from .visitor_log_api import visitor_log_api


def register_redprints(app):
    app.register_blueprint(user_api, url_prefix='/api/users')  # 注册用户管理API
    app.register_blueprint(role_api, url_prefix='/api/roles')  # 注册角色管理API
    app.register_blueprint(permission_api, url_prefix='/api/permissions')  # 注册权限管理API
    app.register_blueprint(user_role_api, url_prefix='/api/users')  # 注册用户角色关联API
    app.register_blueprint(role_permission_api, url_prefix='/api/roles')  # 注册角色权限关联API
    app.register_blueprint(department_api, url_prefix='/api/departments')  # 注册部门管理API
    app.register_blueprint(user_department_api, url_prefix='/api/users')  # 注册用户部门关联API
    app.register_blueprint(campus_api, url_prefix='/api/campuses')  # 注册校区管理API
    app.register_blueprint(visitor_api, url_prefix='/api/visitors')  # 注册访客管理API
    app.register_blueprint(visitor_log_api, url_prefix='/api/visitor_logs')  # 注册访客记录管理API