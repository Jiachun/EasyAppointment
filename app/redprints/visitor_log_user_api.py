# -*- coding: utf-8 -*-
"""
# 文件名称: redprints/visitor_log_user_api.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-11
# 版本: 1.0
# 描述: 普通用户的预约记录 API 接口
"""


from flask import Blueprint, jsonify, request
from app.controllers import VisitorLogUserController


visitor_log_user_api = Blueprint('visitor_log_user_api', __name__)


@visitor_log_user_api.route('/', methods=['GET'])
def get_visitor_logs(current_user):
    """获取所有预约记录的 API 接口"""
    page = int(request.args.get('page', 1))  # 默认为第1页
    per_page = int(request.args.get('per_page', 10))  # 每页默认显示10条
    status = request.args.get('status', 'all')  # 默认所有记录
    response, status_code = VisitorLogUserController.get_all_visitor_logs(current_user, page, per_page, status)
    return jsonify(response), status_code


@visitor_log_user_api.route('/<int:visitor_log_id>', methods=['GET'])
def get_visitor_log_by_id(current_user, visitor_log_id):
    """获取指定预约记录的 API 接口"""
    response, status_code = VisitorLogUserController.get_visitor_log_by_id(current_user, visitor_log_id)
    return jsonify(response), status_code


@visitor_log_user_api.route('/department', methods=['GET'])
def get_visitor_logs_by_department(current_user):
    """根据用户所在部门获取访客记录的 API 接口"""
    page = int(request.args.get('page', 1))  # 默认为第1页
    per_page = int(request.args.get('per_page', 10))  # 每页默认显示10条
    status = request.args.get('status', 'all')  # 默认所有记录
    response, status_code = VisitorLogUserController.get_visitor_logs_by_department(current_user, page, per_page, status)
    return jsonify(response), status_code


@visitor_log_user_api.route('/', methods=['POST'])
def create_visitor_log(current_user):
    """新增预约记录的 API 接口"""
    data = request.json
    response, status_code = VisitorLogUserController.create_visitor_log(current_user, data)
    return jsonify(response), status_code


@visitor_log_user_api.route('/<int:visitor_log_id>', methods=['PUT'])
def update_visitor_log(current_user, visitor_log_id):
    """修改预约记录的 API 接口"""
    data = request.json
    response, status_code = VisitorLogUserController.update_visitor_log(current_user, visitor_log_id, data)
    return jsonify(response), status_code


@visitor_log_user_api.route('/<int:visitor_log_id>', methods=['DELETE'])
def cancel_visitor_log(current_user, visitor_log_id):
    """取消预约记录的 API 接口"""
    response, status_code = VisitorLogUserController.cancel_visitor_log(current_user, visitor_log_id)
    return jsonify(response), status_code
