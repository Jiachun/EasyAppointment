# -*- coding: utf-8 -*-
"""
# 文件名称: blueprints/admin/campus_views.py
# 作者: 李业
# 创建日期: 2024-10-01
# 版本: 1.0
# 描述: 校区管理蓝图
"""


from flask import Blueprint, render_template
from app.controllers import CampusController


campus_blueprint = Blueprint('campus_blueprint', __name__)


campuses = []


@campus_blueprint.route('/', methods=['GET'])
def list_campuses():
    """查询校区列表"""
    return render_template('admin/manage_campuses.html', campuses=campuses)