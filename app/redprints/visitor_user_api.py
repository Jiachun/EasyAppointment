# -*- coding: utf-8 -*-
"""
# 文件名称: redprints/visitor_user_api.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-10
# 版本: 1.0
# 描述: 普通用户的访客信息 API 接口
"""


from flask import Blueprint, jsonify, request
from app.controllers import VisitorUserController


visitor_user_api = Blueprint('visitor_user_api', __name__)


@visitor_user_api.route('/', methods=['GET'])
def get_visitors(current_user):
    """获取当前用户的所有访客信息的 API 接口"""
    response, status_code = VisitorUserController.get_all_visitors(current_user)
    return jsonify(response), status_code


@visitor_user_api.route('/<int:visitor_id>', methods=['GET'])
def get_visitor(current_user, visitor_id):
    """根据访客ID获取访客信息的 API 接口"""
    response, status_code = VisitorUserController.get_visitor_by_id(current_user, visitor_id)
    return jsonify(response), status_code


@visitor_user_api.route('/', methods=['POST'])
def create_visitor(current_user):
    """为当前用户添加访客信息的 API 接口"""
    data = request.json
    response, status_code = VisitorUserController.create_visitor(current_user, data)
    return jsonify(response), status_code


@visitor_user_api.route('/<int:visitor_id>', methods=['DELETE'])
def delete_visitor(current_user, visitor_id):
    """根据访客ID删除访客信息的 API 接口"""
    response, status_code = VisitorUserController.delete_visitor(current_user, visitor_id)
    return jsonify(response), status_code