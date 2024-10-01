"""
# 文件名称: blueprints/campus_api.py
# 作者: 李业
# 创建日期: 2024-10-1
# 版本: 1.0
# 描述: 校区红图
"""

from flask import Blueprint, jsonify, request
from app.controllers import CampusController

campus_api = Blueprint('campus_api', __name__)


@campus_api.route('/campus', methods=['GET'])
def get_campus():
    """获取所有校区信息的API接口"""
    campus = CampusController.get_all_campus()
    return jsonify([campus.to_dic() for campus in campus])


@campus_api.route('/', methods=['POST'])
def create_campus():
    """创建新校区的API接口"""
    data = request.json
    campus = CampusController.create_campus(
        campus_name=data['name'],
        description=data['description'],
    )
    return jsonify(campus.to_dic())


@campus_api.route('/<int:campus_id>', methods=['GET'])
def gt_campus(campus_id):
    """根据校区ID获取校区信息的API接口"""
    campus = CampusController.get_campus_by_id(campus_id)
    if campus:
        return jsonify(campus.to_dic())
    return jsonify({'error': 'Campus not found'}), 404


@campus_api.route('/<int:campus_id>', methods=['DELETE'])
def delete_campus(campus_id):
    """根据校区ID删除校区的API接口"""
    success = CampusController.delete_campus(campus_id)
    if success:
        return jsonify({'message': 'Campus deleted successfully'})
    return jsonify({'error': 'Campus not found'}), 404
