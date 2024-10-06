# -*- coding: utf-8 -*-
"""
# 文件名称: redprints/auth_api.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-06
# 版本: 1.0
# 描述: 认证与授权 API 接口
"""

from flask import Blueprint, jsonify, request
from app.controllers.auth_controller import AuthController

auth_api = Blueprint('auth_api', __name__)


@auth_api.route('/login', methods=['POST'])
def login():
    """用户登录认证的 API 接口"""
    data = request.json
    response, status_code = AuthController.login(data)
    return jsonify(response), status_code