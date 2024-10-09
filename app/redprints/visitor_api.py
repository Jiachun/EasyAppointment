# -*- coding: utf-8 -*-
"""
# 文件名称: redprints/visitor_api.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-04
# 版本: 1.0
# 描述: 访客信息 API 接口
"""


from flask import Blueprint, jsonify, request
from app.controllers import VisitorController

visitor_api = Blueprint('visitor_api', __name__)


@visitor_api.route('/', methods=['GET'])
def get_visitors():
    """获取所有访客信息的 API 接口"""
    page = int(request.args.get('page', 1))  # 默认为第1页
    per_page = int(request.args.get('per_page', 10))  # 每页默认显示10条
    response, status_code = VisitorController.get_all_visitors(page, per_page)
    return jsonify(response), status_code


@visitor_api.route('/<int:visitor_id>', methods=['GET'])
def get_visitor(visitor_id):
    """根据访客ID获取访客信息的 API 接口"""
    response, status_code = VisitorController.get_visitor_by_id(visitor_id)
    return jsonify(response), status_code


@visitor_api.route('/', methods=['POST'])
def create_visitor():
    """创建新访客的 API 接口"""
    data = request.json
    response, status_code = VisitorController.create_visitor(data)
    return jsonify(response), status_code


@visitor_api.route('/<int:visitor_id>', methods=['PUT'])
def update_visitor(visitor_id):
    """根据访客ID修改访客信息的 API 接口"""
    data = request.json
    response, status_code = VisitorController.update_visitor(visitor_id, data)
    return jsonify(response), status_code


@visitor_api.route('/<int:visitor_id>', methods=['DELETE'])
def delete_visitor(visitor_id):
    """根据访客ID删除访客的 API 接口"""
    response, status_code = VisitorController.delete_visitor(visitor_id)
    return jsonify(response), status_code


@visitor_api.route('/search', methods=['GET'])
def search_visitors():
    """检索访客信息的 API 接口"""
    data = request.args.get('data')  # 从查询参数获取 JSON 字符串
    page = int(request.args.get('page', 1))  # 默认为第1页
    per_page = int(request.args.get('per_page', 10))  # 每页默认显示10条
    response, status_code = VisitorController.search_visitors(data, page, per_page)
    return jsonify(response), status_code