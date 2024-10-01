# -*- coding: utf-8 -*-
"""
# 文件名称: blueprints/user_api.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-01
# 版本: 1.0
# 描述: 用户红图。
"""


from flask import Blueprint, jsonify, request
from app.controllers import UserController


user_api = Blueprint('user_api', __name__)


@user_api.route('/', methods=['GET'])
def get_users():
    """获取所有用户信息的 API 接口"""
    users = UserController.get_all_users()
    return jsonify([user.to_dict() for user in users])


@user_api.route('/', methods=['POST'])
def create_user():
    """创建新用户的 API 接口"""
    data = request.json
    user = UserController.create_user(
        username=data['username'],
        email=data['email'],
        password_hash=data['password_hash']
    )
    return jsonify(user.to_dict()), 201


@user_api.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """根据用户ID获取用户信息的 API 接口"""
    user = UserController.get_user_by_id(user_id)
    if user:
        return jsonify(user.to_dict())
    return jsonify({'error': 'User not found'}), 404


@user_api.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """根据用户ID删除用户的 API 接口"""
    success = UserController.delete_user(user_id)
    if success:
        return jsonify({'message': 'User deleted successfully'})
    return jsonify({'error': 'User not found'}), 404