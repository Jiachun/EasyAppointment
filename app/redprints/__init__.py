from .auth_api import auth_api
from .campus_api import campus_api
from .department_api import department_api
from .permission_api import permission_api
from .role_api import role_api
from .role_permission_api import role_permission_api
from .user_api import user_api
from .user_department_api import user_department_api
from .user_profile_api import user_profile_api
from .user_role_api import user_role_api
from .visitor_admin_api import visitor_admin_api
from .visitor_log_admin_api import visitor_log_admin_api
from .visitor_log_user_api import visitor_log_user_api
from .visitor_user_api import visitor_user_api


def register_redprints(app):
    app.register_blueprint(campus_api, url_prefix='/api/campuses')  # 注册校区信息管理的 API 接口
    app.register_blueprint(department_api, url_prefix='/api/departments')  # 注册部门信息管理的 API 接口
    app.register_blueprint(permission_api, url_prefix='/api/permissions')  # 注册权限信息管理的 API 接口
    app.register_blueprint(role_api, url_prefix='/api/roles')  # 注册角色信息管理的 API 接口
    app.register_blueprint(role_permission_api, url_prefix='/api/roles')  # 注册角色和权限关联的 API 接口
    app.register_blueprint(user_api, url_prefix='/api/users')  # 注册用户管理API
    app.register_blueprint(user_role_api, url_prefix='/api/users')  # 注册用户角色关联API
    app.register_blueprint(user_department_api, url_prefix='/api/users')  # 注册用户部门关联API
    app.register_blueprint(visitor_admin_api, url_prefix='/api/visitors_admin')  # 注册管理员的访客信息管理API
    app.register_blueprint(visitor_log_admin_api, url_prefix='/api/visitor_logs_admin')  # 注册管理员的访客记录管理API
    app.register_blueprint(auth_api, url_prefix='/api/auth')  # 注册认证与授权API
    app.register_blueprint(user_profile_api, url_prefix='/api/user_profile')  # 注册用户的个人信息管理API
    app.register_blueprint(visitor_user_api, url_prefix='/api/visitors_user')  # 注册普通用户的访客信息管理API
    app.register_blueprint(visitor_log_user_api, url_prefix='/api/visitor_logs_user')  # 注册普通用户的预约记录管理API
