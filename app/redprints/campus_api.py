# -*- coding: utf-8 -*-
"""
# 文件名称: redprints/campus_api.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-10
# 版本: 1.0
# 描述: 校区信息 API 接口
"""


import json
from flask import Blueprint, jsonify, request
from app.controllers import CampusController
from utils.crypto_utils import aes256_encrypt_data


campus_api = Blueprint('campus_api', __name__)


@campus_api.route('/', methods=['GET'])
def get_campuses():
    """获取所有校区信息的 API 接口"""
    page = int(request.args.get('page', 1))  # 默认为第1页
    per_page = int(request.args.get('per_page', 10))  # 每页默认显示10条
    response, status_code = CampusController.get_all_campuses(page, per_page)
    # return jsonify(aes256_encrypt_data(json.dumps(response))), status_code
    return jsonify(response), status_code


@campus_api.route('/<int:campus_id>', methods=['GET'])
def get_campus(campus_id):
    """根据校区ID获取校区信息的 API 接口"""
    response, status_code = CampusController.get_campus_by_id(campus_id)
    return jsonify(response), status_code


@campus_api.route('/', methods=['POST'])
def create_campus():
    """创建新校区的 API 接口"""
    data = request.json
    response, status_code = CampusController.create_campus(data)
    return jsonify(response), status_code


@campus_api.route('/<int:campus_id>', methods=['PUT'])
def update_campus(campus_id):
    """根据校区ID修改校区信息的 API 接口"""
    data = request.json
    response, status_code = CampusController.update_campus(campus_id, data)
    return jsonify(response), status_code


@campus_api.route('/<int:campus_id>', methods=['DELETE'])
def delete_campus(campus_id):
    """根据校区ID删除校区的 API 接口"""
    response, status_code = CampusController.delete_campus(campus_id)
    return jsonify(response), status_code


@campus_api.route('/search', methods=['GET'])
def search_campuses():
    """检索校区信息的 API 接口"""
    filters = request.args.get('filters')  # 从查询参数获取 JSON 字符串
    page = int(request.args.get('page', 1))  # 默认为第1页
    per_page = int(request.args.get('per_page', 10))  # 每页默认显示10条
    sort_field = request.args.get('sort_field', 'id')  # 默认按id排序
    sort_order = request.args.get('sort_order', 'asc')  # 默认升序
    response, status_code = CampusController.search_campuses(filters, page, per_page, sort_field, sort_order)
    return jsonify(response), status_code