# -*- coding: utf-8 -*-
"""
# 文件名称: redprints/visitor_log_admin_api.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-04
# 版本: 1.0
# 描述: 管理员的访客记录管理的 API 接口
"""

from flask import Blueprint, jsonify, request

from app.controllers import VisitorLogAdminController

visitor_log_admin_api = Blueprint('visitor_log_admin_api', __name__)


@visitor_log_admin_api.route('/', methods=['GET'])
def get_visitor_logs():
    """获取所有访客记录的 API 接口"""
    page = int(request.args.get('page', 1))  # 默认为第1页
    per_page = int(request.args.get('per_page', 10))  # 每页默认显示10条
    response, status_code = VisitorLogAdminController.get_all_visitor_logs(page, per_page)
    return jsonify(response), status_code


@visitor_log_admin_api.route('/<int:visitor_log_id>', methods=['GET'])
def get_visitor_log(visitor_log_id):
    """根据访客记录ID获取访客记录的 API 接口"""
    response, status_code = VisitorLogAdminController.get_visitor_log_by_id(visitor_log_id)
    return jsonify(response), status_code


@visitor_log_admin_api.route('/', methods=['POST'])
def create_visitor_log():
    """创建新访客的 API 接口"""
    data = request.json
    response, status_code = VisitorLogAdminController.create_visitor_log(data)
    return jsonify(response), status_code


@visitor_log_admin_api.route('/<int:visitor_log_id>', methods=['PUT'])
def update_visitor_log(visitor_log_id):
    """根据访客记录ID修改访客记录的 API 接口"""
    data = request.json
    response, status_code = VisitorLogAdminController.update_visitor_log(visitor_log_id, data)
    return jsonify(response), status_code


@visitor_log_admin_api.route('/<int:visitor_log_id>', methods=['DELETE'])
def delete_visitor_log(visitor_log_id):
    """根据访客记录ID删除访客的 API 接口"""
    response, status_code = VisitorLogAdminController.delete_visitor_log(visitor_log_id)
    return jsonify(response), status_code


@visitor_log_admin_api.route('/search', methods=['GET'])
def search_visitor_logs():
    """检索访客记录的 API 接口"""
    filters = request.args.get('filters')  # 从查询参数获取 JSON 字符串
    page = int(request.args.get('page', 1))  # 默认为第1页
    per_page = int(request.args.get('per_page', 10))  # 每页默认显示10条
    sort_field = request.args.get('sort_field', 'id')  # 默认按id排序
    sort_order = request.args.get('sort_order', 'asc')  # 默认升序
    response, status_code = VisitorLogAdminController.search_visitor_logs(filters, page, per_page, sort_field,
                                                                          sort_order)
    return jsonify(response), status_code


@visitor_log_admin_api.route('/<int:visitor_log_id>/approve', methods=['POST'])
def approve_visitor_log(current_user, visitor_log_id):
    """审批预约记录的 API 接口"""
    data = request.json
    response, status_code = VisitorLogAdminController.approve_visitor_log(current_user, visitor_log_id, data)
    return jsonify(response), status_code


@visitor_log_admin_api.route('/<int:visitor_log_id>/verify', methods=['POST'])
def verify_visitor_log(current_user, visitor_log_id):
    """来访登记的 API 接口"""
    response, status_code = VisitorLogAdminController.verify_visitor_log(current_user, visitor_log_id)
    return jsonify(response), status_code
