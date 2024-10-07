# -*- coding: utf-8 -*-
"""
# 文件名称: utils/permission_decorator.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-07
# 版本: 1.0
# 描述: 权限验证装饰器。
"""


from functools import wraps
from flask import jsonify


def permission_required(required_permission):
    """权限鉴定装饰器，验证用户是否具有指定权限"""

    def decorator(f):
        @wraps(f)
        def wrapper(current_user, *args, **kwargs):
            # 检查当前用户是否拥有所需的权限
            if not current_user.has_permission(required_permission):
                return jsonify({'error': '权限不足，无法访问该资源'}), 403

            # 如果权限验证通过，继续执行被装饰的函数
            return f(current_user, *args, **kwargs)

        return wrapper
    return decorator