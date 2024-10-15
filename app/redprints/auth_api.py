# -*- coding: utf-8 -*-
"""
# 文件名称: redprints/auth_api.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-06
# 版本: 1.0
# 描述: 认证与授权 API 接口
"""

from flask import Blueprint, jsonify, request

from app.controllers import AuthController
from utils.decorators import token_required

auth_api = Blueprint('auth_api', __name__)


@auth_api.route('/login', methods=['POST'])
def login():
    """用户登录认证的 API 接口"""
    data = request.json
    response, status_code = AuthController.login(data)
    return jsonify(response), status_code


@auth_api.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    """用户注销的 API 接口"""
    response, status_code = AuthController.logout(current_user)
    return jsonify(response), status_code


@auth_api.route('/permissions', methods=['POST'])
@token_required
def get_permissions(current_user):
    """获取用户权限列表的 API 接口"""
    data = request.json
    response, status_code = AuthController.get_permissions(current_user, data)
    return jsonify(response), status_code


@auth_api.route('/change_password', methods=['POST'])
@token_required
def change_password(current_user):
    """修改密码的 API 接口"""
    data = request.json
    response, status_code = AuthController.change_password(current_user, data)
    return jsonify(response), status_code


@auth_api.route('/set_password', methods=['POST'])
@token_required
def set_password():
    """设置密码的 API 接口"""
    data = request.json
    response, status_code = AuthController.set_password(data)
    return jsonify(response), status_code


@auth_api.route('/register', methods=['POST'])
def wechat_login():
    """微信小程序登录的 API 接口"""
    data = request.json
    response, status_code = AuthController.wechat_login(data)
    return jsonify(response), status_code


@auth_api.route('/bind', methods=['POST'])
def bind_user():
    """微信小程序绑定用户的 API 接口"""
    data = request.json
    response, status_code = AuthController.bind_user(data)
    return jsonify(response), status_code


@auth_api.route('/unbind', methods=['POST'])
@token_required
def unbind_user():
    """用户解绑的 API 接口"""
    data = request.json
    response, status_code = AuthController.unbind_user(data)
    return jsonify(response), status_code


@auth_api.route('/unregister', methods=['POST'])
@token_required
def unregister(current_user):
    """清除用户数据的 API 接口"""
    data = request.json
    response, status_code = AuthController.unregister(current_user, data)
    return jsonify(response), status_code


@auth_api.route('/activate', methods=['POST'])
@token_required
def activate_user():
    """激活用户的 API 接口"""
    data = request.json
    response, status_code = AuthController.activate_user(data)
    return jsonify(response), status_code


@auth_api.route('/deactivate', methods=['POST'])
@token_required
def deactivate_user():
    """停用用户的 API 接口"""
    data = request.json
    response, status_code = AuthController.deactivate_user(data)
    return jsonify(response), status_code
