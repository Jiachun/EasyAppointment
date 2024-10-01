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


# 根据多条件搜索用户，支持分页
@user_api.route('/search', methods=['GET'])
def search_users():
    name = request.args.get('name')
    phone = request.args.get('phone')
    id_number = request.args.get('id_number')
    gender = request.args.get('gender')

    # 获取分页参数
    try:
        page = int(request.args.get('page', 1))  # 默认为第1页
        per_page = int(request.args.get('per_page', 10))  # 每页默认显示10条
    except ValueError:
        return jsonify({"message": "Invalid pagination parameters"}), 400

    users, total_pages = UserController.search_users(name, phone, id_number, gender, page, per_page)

    return jsonify({
        "users": [user.to_dict() for user in users],
        "total_pages": total_pages,
        "current_page": page,
        "per_page": per_page
    })