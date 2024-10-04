# -*- coding: utf-8 -*-
"""
# 文件名称: redprints/user_department_api.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-04
# 版本: 1.0
# 描述: 用户部门关联 API 接口
"""


from flask import Blueprint, jsonify, request
from app.controllers import UserDepartmentController


user_department_api = Blueprint('user_department_api', __name__)


@user_department_api.route('/<int:user_id>/departments', methods=['GET'])
def get_user_departments(user_id):
    """获取用户的所有部门"""
    response, status_code = UserDepartmentController.get_departments_by_user(user_id)
    return jsonify(response), status_code


# 为用户添加部门
@user_department_api.route('/<int:user_id>/departments', methods=['POST'])
def add_department_to_user(user_id):
    """为用户添加部门"""
    data = request.json
    response, status_code = UserDepartmentController.add_department_to_user(user_id, data.get('department_id', None))
    return jsonify(response), status_code


# 从用户中移除部门
@user_department_api.route('/<int:user_id>/departments', methods=['DELETE'])
def remove_department_from_user(user_id):
    """从用户中移除部门"""
    data = request.get_json()
    response, status_code = UserDepartmentController.remove_department_from_user(user_id, data.get('department_id', None))
    return jsonify(response), status_code