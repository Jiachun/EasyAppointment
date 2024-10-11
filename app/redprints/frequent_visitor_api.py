# -*- coding: utf-8 -*-
"""
# 文件名称: redprints/frequent_visitor_api.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-10
# 版本: 1.0
# 描述: 常用访客信息 API 接口
"""


from flask import Blueprint, jsonify, request
from app.controllers import FrequentVisitorController


frequent_visitor_api = Blueprint('frequent_visitor_api', __name__)


@frequent_visitor_api.route('/', methods=['GET'])
def get_frequent_visitors(current_user):
    """获取当前用户的常用访客信息的 API 接口"""
    response, status_code = FrequentVisitorController.get_frequent_visitors(current_user)
    return jsonify(response), status_code


@frequent_visitor_api.route('/<int:visitor_id>', methods=['GET'])
def get_frequent_visitor(current_user, visitor_id):
    """根据访客ID获取当前用户的常用访客信息的 API 接口"""
    response, status_code = FrequentVisitorController.get_frequent_visitor(current_user, visitor_id)
    return jsonify(response), status_code


@frequent_visitor_api.route('/', methods=['POST'])
def create_frequent_visitor(current_user):
    """为当前用户添加常用访客信息的 API 接口"""
    data = request.json
    response, status_code = FrequentVisitorController.create_frequent_visitor(current_user, data)
    return jsonify(response), status_code


@frequent_visitor_api.route('/<int:visitor_id>', methods=['DELETE'])
def delete_frequent_visitor(current_user, visitor_id):
    """为当前用户移除常用访客信息的 API 接口"""
    response, status_code = FrequentVisitorController.delete_frequent_visitor(current_user, visitor_id)
    return jsonify(response), status_code