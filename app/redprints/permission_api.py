# -*- coding: utf-8 -*-
"""
# 文件名称: blueprints/permission_api.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-04
# 版本: 1.0
# 描述: 权限信息 API 接口
"""


from flask import Blueprint, jsonify, request
from app.controllers import PermissionController


permission_api = Blueprint('permission_api', __name__)


@permission_api.route('/', methods=['GET'])
def get_permissions():
    """获取所有权限信息的 API 接口"""
    page = int(request.args.get('page', 1))  # 默认为第1页
    per_page = int(request.args.get('per_page', 10))  # 每页默认显示10条
    response, status_code = PermissionController.get_all_permissions(page, per_page)
    return jsonify(response), status_code


@permission_api.route('/<int:permission_id>', methods=['GET'])
def get_permission(permission_id):
    """根据权限ID获取权限信息的 API 接口"""
    response, status_code = PermissionController.get_permission_by_id(permission_id)
    return jsonify(response), status_code


@permission_api.route('/', methods=['POST'])
def create_permission():
    """创建新权限的 API 接口"""
    data = request.json
    response, status_code = PermissionController.create_permission(data)
    return jsonify(response), status_code


@permission_api.route('/<int:permission_id>', methods=['PUT'])
def update_permission(permission_id):
    """根据权限ID修改权限信息的 API 接口"""
    data = request.json
    response, status_code = PermissionController.update_permission(permission_id, data)
    return jsonify(response), status_code


@permission_api.route('/<int:permission_id>', methods=['DELETE'])
def delete_permission(permission_id):
    """根据权限ID删除权限的 API 接口"""
    response, status_code = PermissionController.delete_permission(permission_id)
    return jsonify(response), status_code