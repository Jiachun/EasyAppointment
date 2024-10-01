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

    # 获取分页参数
    try:
        page = int(request.args.get('page', 1))  # 默认为第1页
        per_page = int(request.args.get('per_page', 10))  # 每页默认显示10条
    except ValueError:
        return jsonify({"message": "Invalid pagination parameters"}), 400

    campuses, total_pages = CampusController.get_all_campuses(page, per_page)

    return jsonify({
        "campuses": [campus.to_dict() for campus in campuses],
        "total_pages": total_pages,
        "current_page": page,
        "per_page": per_page
    })


@campus_api.route('/<int:campus_id>', methods=['GET'])
def get_campus(campus_id):
    """根据校区ID获取校区信息的 API 接口"""
    campus = CampusController.get_campus_by_id(campus_id)
    if campus:
        return jsonify(campus.to_dict())
    return jsonify({'error': 'Campus not found'}), 404


@campus_api.route('/', methods=['POST'])
def create_campus():
    """创建新校区的 API 接口"""
    data = request.json
    new_campus = CampusController.create_campus(
        name=data['name'],
        description=data['description'],
    )
    return jsonify(new_campus.to_dict()), 201


@campus_api.route('/<int:campus_id>', methods=['PUT'])
def update_campus(campus_id):
    """根据校区ID修改校区信息的 API 接口"""
    data = request.json
    updated_campus = CampusController.update_campus(campus_id, **data)

    if not updated_campus:
        return jsonify({"message": "User not found"}), 404

    return jsonify(updated_campus.to_dict()), 200


@campus_api.route('/<int:campus_id>', methods=['DELETE'])
def delete_campus(campus_id):
    """根据校区ID删除校区的 API 接口"""
    deleted = CampusController.delete_campus(campus_id)
    if deleted:
        return jsonify({'message': 'Campus deleted successfully'})
    return jsonify({'error': 'Campus not found'}), 404
