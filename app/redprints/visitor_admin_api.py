# -*- coding: utf-8 -*-
"""
# 文件名称: redprints/visitor_admin_api.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-04
# 版本: 1.0
# 描述: 管理员的访客信息管理的 API 接口
"""

from flask import Blueprint, jsonify, request

from app.controllers import VisitorAdminController

visitor_admin_api = Blueprint('visitor_admin_api', __name__)


@visitor_admin_api.route('/', methods=['GET'])
def get_visitors():
    """根据用户ID获取指定用户的所有访客信息的 API 接口"""
    page = int(request.args.get('page', 1))  # 默认为第1页
    per_page = int(request.args.get('per_page', 10))  # 每页默认显示10条
    response, status_code = VisitorAdminController.get_all_visitors(page, per_page)
    return jsonify(response), status_code


@visitor_admin_api.route('/<int:visitor_id>', methods=['GET'])
def get_visitor(visitor_id):
    """根据访客ID获取访客信息的 API 接口"""
    response, status_code = VisitorAdminController.get_visitor_by_id(visitor_id)
    return jsonify(response), status_code


@visitor_admin_api.route('/', methods=['POST'])
def create_visitor():
    """创建新访客的 API 接口"""
    data = request.json
    response, status_code = VisitorAdminController.create_visitor(data)
    return jsonify(response), status_code


@visitor_admin_api.route('/<int:visitor_id>', methods=['PUT'])
def update_visitor(visitor_id):
    """根据访客ID修改访客信息的 API 接口"""
    data = request.json
    response, status_code = VisitorAdminController.update_visitor(visitor_id, data)
    return jsonify(response), status_code


@visitor_admin_api.route('/<int:visitor_id>', methods=['DELETE'])
def delete_visitor(visitor_id):
    """根据访客ID删除访客的 API 接口"""
    response, status_code = VisitorAdminController.delete_visitor(visitor_id)
    return jsonify(response), status_code


@visitor_admin_api.route('/search', methods=['GET'])
def search_visitors():
    """检索访客信息的 API 接口"""
    filters = request.args.get('filters')  # 从查询参数获取 JSON 字符串
    page = int(request.args.get('page', 1))  # 默认为第1页
    per_page = int(request.args.get('per_page', 10))  # 每页默认显示10条
    sort_field = request.args.get('sort_field', 'id')  # 默认按id排序
    sort_order = request.args.get('sort_order', 'asc')  # 默认升序
    response, status_code = VisitorAdminController.search_visitors(filters, page, per_page, sort_field, sort_order)
    return jsonify(response), status_code
