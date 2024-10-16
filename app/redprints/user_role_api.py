# -*- coding: utf-8 -*-
"""
# 文件名称: redprints/user_role_api.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-04
# 版本: 1.0
# 描述: 用户和角色关联的 API 接口
"""

from flask import Blueprint, jsonify, request

from app.controllers import UserRoleController

user_role_api = Blueprint('user_role_api', __name__)


@user_role_api.route('/<int:user_id>/roles', methods=['GET'])
def get_user_roles(user_id):
    """获取用户的所有角色"""
    response, status_code = UserRoleController.get_roles_by_user(user_id)
    return jsonify(response), status_code


# 为用户添加角色
@user_role_api.route('/<int:user_id>/roles', methods=['POST'])
def add_roles_to_user(user_id):
    """为用户添加角色"""
    data = request.json
    response, status_code = UserRoleController.add_roles_to_user(user_id, data.get('role_ids', []))
    return jsonify(response), status_code


# 从用户中移除角色
@user_role_api.route('/<int:user_id>/roles', methods=['DELETE'])
def remove_roles_from_user(user_id):
    """从用户中移除角色"""
    data = request.get_json()
    response, status_code = UserRoleController.remove_roles_from_user(user_id, data.get('role_ids', []))
    return jsonify(response), status_code
