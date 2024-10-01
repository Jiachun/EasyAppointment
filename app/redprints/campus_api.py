# -*- coding: utf-8 -*-
"""
# 文件名称: redprints/campus_api.py
# 作者: 李业
# 创建日期: 2024-10-01
# 版本: 1.0
# 描述: 校区红图
"""

from flask import Blueprint, jsonify, request
from app.controllers import CampusController


campus_api = Blueprint('campus_api', __name__)


@campus_api.route('/', methods=['GET'])
def get_campuses():
    """获取所有校区信息的 API 接口"""
    campuses = CampusController.get_all_campuses()
    return jsonify([campus.to_dict() for campus in campuses])


@campus_api.route('/', methods=['POST'])
def create_campus():
    """创建新校区的 API 接口"""
    data = request.json
    campus = CampusController.create_campus(
        name=data['name'],
        description=data['description'],
    )
    return jsonify(campus.to_dict()), 201


@campus_api.route('/<int:campus_id>', methods=['GET'])
def gt_campus(campus_id):
    """根据校区ID获取校区信息的 API 接口"""
    campus = CampusController.get_campus_by_id(campus_id)
    if campus:
        return jsonify(campus.to_dict())
    return jsonify({'error': 'Campus not found'}), 404


@campus_api.route('/<int:campus_id>', methods=['DELETE'])
def delete_campus(campus_id):
    """根据校区ID删除校区的 API 接口"""
    success = CampusController.delete_campus(campus_id)
    if success:
        return jsonify({'message': 'Campus deleted successfully'})
    return jsonify({'error': 'Campus not found'}), 404
