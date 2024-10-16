# -*- coding: utf-8 -*-
"""
# 文件名称: redprints/department_api.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-04
# 版本: 1.0
# 描述: 部门信息管理的 API 接口
"""

from flask import Blueprint, jsonify, request

from app.controllers import DepartmentController

department_api = Blueprint('department_api', __name__)


@department_api.route('/', methods=['GET'])
def get_departments():
    """获取所有部门信息的 API 接口"""
    page = int(request.args.get('page', 1))  # 默认为第1页
    per_page = int(request.args.get('per_page', 10))  # 每页默认显示10条
    response, status_code = DepartmentController.get_all_departments(page, per_page)
    return jsonify(response), status_code


@department_api.route('/<int:department_id>', methods=['GET'])
def get_department(department_id):
    """根据部门ID获取部门信息的 API 接口"""
    response, status_code = DepartmentController.get_department_by_id(department_id)
    return jsonify(response), status_code


@department_api.route('/', methods=['POST'])
def create_department():
    """创建新部门的 API 接口"""
    data = request.json
    response, status_code = DepartmentController.create_department(data)
    return jsonify(response), status_code


@department_api.route('/<int:department_id>', methods=['PUT'])
def update_department(department_id):
    """根据部门ID修改部门信息的 API 接口"""
    data = request.json
    response, status_code = DepartmentController.update_department(department_id, data)
    return jsonify(response), status_code


@department_api.route('/<int:department_id>', methods=['DELETE'])
def delete_department(department_id):
    """根据部门ID删除部门的 API 接口"""
    response, status_code = DepartmentController.delete_department(department_id)
    return jsonify(response), status_code


@department_api.route('/search', methods=['GET'])
def search_departments():
    """检索部门信息的 API 接口"""
    filters = request.args.get('filters')  # 从查询参数获取 JSON 字符串
    page = int(request.args.get('page', 1))  # 默认为第1页
    per_page = int(request.args.get('per_page', 10))  # 每页默认显示10条
    sort_field = request.args.get('sort_field', 'id')  # 默认按id排序
    sort_order = request.args.get('sort_order', 'asc')  # 默认升序
    response, status_code = DepartmentController.search_departments(filters, page, per_page, sort_field, sort_order)
    return jsonify(response), status_code
