# -*- coding: utf-8 -*-
"""
# 文件名称: blueprints/admin/user_views.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-01
# 版本: 1.0
# 描述: 用户管理蓝图。
"""


from flask import Blueprint, render_template
from app.controllers import UserController


user_blueprint = Blueprint('user_blueprint', __name__)


users = []


@user_blueprint.route('/', methods=['GET'])
def list_users():
    """查询用户列表"""
    return render_template('admin/manage_users.html', users=users)