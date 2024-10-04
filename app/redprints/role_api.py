# -*- coding: utf-8 -*-
"""
# 文件名称: redprints/role_api.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-04
# 版本: 1.0
# 描述: 角色信息 API 接口
"""


from flask import Blueprint, jsonify, request
from app.controllers import RoleController


role_api = Blueprint('role_api', __name__)


@role_api.route('/', methods=['GET'])
def get_roles():
    """获取所有角色信息的 API 接口"""
    page = int(request.args.get('page', 1))  # 默认为第1页
    per_page = int(request.args.get('per_page', 10))  # 每页默认显示10条
    response, status_code = RoleController.get_all_roles(page, per_page)
    return jsonify(response), status_code


@role_api.route('/<int:role_id>', methods=['GET'])
def get_role(role_id):
    """根据角色ID获取角色信息的 API 接口"""
    response, status_code = RoleController.get_role_by_id(role_id)
    return jsonify(response), status_code


@role_api.route('/', methods=['POST'])
def create_role():
    """创建新角色的 API 接口"""
    data = request.json
    response, status_code = RoleController.create_role(data)
    return jsonify(response), status_code


@role_api.route('/<int:role_id>', methods=['PUT'])
def update_role(role_id):
    """根据角色ID修改角色信息的 API 接口"""
    data = request.json
    response, status_code = RoleController.update_role(role_id, data)
    return jsonify(response), status_code


@role_api.route('/<int:role_id>', methods=['DELETE'])
def delete_role(role_id):
    """根据角色ID删除角色的 API 接口"""
    response, status_code = RoleController.delete_role(role_id)
    return jsonify(response), status_code