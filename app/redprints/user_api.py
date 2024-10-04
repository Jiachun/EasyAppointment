# -*- coding: utf-8 -*-
"""
# 文件名称: redprints/user_api.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-01
# 版本: 1.0
# 描述: 用户信息 API 接口
"""


from flask import Blueprint, jsonify, request
from app.controllers import UserController


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