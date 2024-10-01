"""
# 文件名称:blueprints.campus_views
# 作者:李业
# 创建日期:2024-10-1
# 版本:1.0
# 描述:校区管理蓝图
"""

from flask import Blueprint, render_template
from app.controllers import CampusController

campus_views = Blueprint('campus_views', __name__)

campus = [{'id': 1, 'name': 'Blice'},{'id': 2, 'name': 'Blake'},{'id': 3, 'name': 'Blake'}]


@campus_views.route('/', methods=['GET'])
def list_campus():
    return render_template('campus/list.html', campus=campus)