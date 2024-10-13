# -*- coding: utf-8 -*-
"""
# 文件名称: redprints/role_permission_api.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-04
# 版本: 1.0
# 描述: 角色权限关联的 API 接口
"""

from flask import Blueprint, jsonify, request

from app.controllers import RolePermissionController

role_permission_api = Blueprint('role_permission_api', __name__)


@role_permission_api.route('/<int:role_id>/permissions', methods=['GET'])
def get_role_permissions(role_id):
    """获取角色的所有权限"""
    response, status_code = RolePermissionController.get_permissions_by_role(role_id)
    return jsonify(response), status_code


@role_permission_api.route('/<int:role_id>/permissions', methods=['POST'])
def add_permissions_to_role(role_id):
    """为角色添加权限"""
    data = request.json
    response, status_code = RolePermissionController.add_permissions_to_role(role_id, data.get('permission_ids', []))
    return jsonify(response), status_code


@role_permission_api.route('/<int:role_id>/permissions', methods=['DELETE'])
def remove_permissions_from_role(role_id):
    """从角色中移除权限"""
    data = request.get_json()
    response, status_code = RolePermissionController.remove_permissions_from_role(role_id,
                                                                                  data.get('permission_ids', []))
    return jsonify(response), status_code
