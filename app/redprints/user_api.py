# -*- coding: utf-8 -*-
"""
# 文件名称: redprints/user_api.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-01
# 版本: 1.0
# 描述: 用户信息 API 接口
"""


from flask import Blueprint, jsonify, request
from app.controllers import UserController, VisitorAdminController, DepartmentController


user_api = Blueprint('user_api', __name__)


@user_api.route('/', methods=['GET'])
def get_users():
    """获取所有用户信息的 API 接口"""
    page = int(request.args.get('page', 1))  # 默认为第1页
    per_page = int(request.args.get('per_page', 10))  # 每页默认显示10条
    response, status_code = UserController.get_all_users(page, per_page)
    return jsonify(response), status_code


@user_api.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """根据用户ID获取用户信息的 API 接口"""
    response, status_code = UserController.get_user_by_id(user_id)
    return jsonify(response), status_code


@user_api.route('/', methods=['POST'])
def create_user():
    """创建新用户的 API 接口"""
    data = request.json
    response, status_code = UserController.create_user(data)
    return jsonify(response), status_code


@user_api.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """根据用户ID修改用户信息的 API 接口"""
    data = request.json
    response, status_code = UserController.update_user(user_id, data)
    return jsonify(response), status_code


@user_api.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """根据用户ID删除用户的 API 接口"""
    response, status_code = UserController.delete_user(user_id)
    return jsonify(response), status_code


@user_api.route('/<int:user_id>/departments', methods=['GET'])
def get_departments(user_id):
    """获取指定用户所有部门信息的 API 接口"""
    response, status_code = DepartmentController.get_departments_by_user(user_id)
    return jsonify(response), status_code


@user_api.route('/<int:user_id>/visitors', methods=['GET'])
def get_visitors(user_id):
    """获取指定用户所有访客信息的 API 接口"""
    response, status_code = VisitorAdminController.get_visitors_by_user(user_id)
    return jsonify(response), status_code


@user_api.route('/search', methods=['GET'])
def search_users():
    """检索用户信息的 API 接口"""
    filters = request.args.get('filters')  # 从查询参数获取 JSON 字符串
    page = int(request.args.get('page', 1))  # 默认为第1页
    per_page = int(request.args.get('per_page', 10))  # 每页默认显示10条
    sort_field = request.args.get('sort_field', 'id')  # 默认按id排序
    sort_order = request.args.get('sort_order', 'asc')  # 默认升序
    response, status_code = UserController.search_users(filters, page, per_page, sort_field, sort_order)
    return jsonify(response), status_code