# -*- coding: utf-8 -*-
"""
# 文件名称: redprints/user_profile_api.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-10
# 版本: 1.0
# 描述: 用户个人信息 API 接口
"""


from flask import Blueprint, jsonify, request
from app.controllers import UserProfileController


user_profile_api = Blueprint('user_profile_api', __name__)


@user_profile_api.route('/', methods=['GET'])
def get_user_profile(current_user):
    """获取当前用户信息的 API 接口"""
    response, status_code = UserProfileController.get_user_profile(current_user)
    return jsonify(response), status_code


@user_profile_api.route('/', methods=['POST'])
def update_user_profile(current_user):
    """更新当前用户信息的 API 接口"""
    data = request.json
    response, status_code = UserProfileController.update_user_profile(current_user, data)
    return jsonify(response), status_code