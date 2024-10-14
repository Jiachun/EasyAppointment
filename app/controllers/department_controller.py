# -*- coding: utf-8 -*-
"""
# 文件名称: controllers/department_controller.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-04
# 版本: 1.0
# 描述: 部门信息管理的逻辑控制器
"""

import json
from datetime import datetime

from sqlalchemy import asc, desc

from app.models import Department
from extensions.db import db
from utils.format_utils import format_response
from utils.validate_utils import validate_department_name


class DepartmentController:
    @staticmethod
    def get_all_departments(page=1, per_page=10):
        """获取所有部门信息"""

        # 分页
        paginated_departments = Department.query.filter_by(is_deleted=False).paginate(page=page, per_page=per_page,
                                                                                      error_out=False)

        # 返回分页后的数据、总页数、当前页和每页记录数
        return format_response(True, {
            "departments": [department.to_dict() for department in paginated_departments.items],
            "total_pages": paginated_departments.pages,
            "current_page": page,
            "per_page": per_page
        }), 200

    @staticmethod
    def get_department_by_id(department_id):
        """根据部门ID获取部门信息"""
        department = Department.query.filter_by(id=department_id, is_deleted=False).first()
        if department:
            return format_response(True, department.to_dict()), 200
        return format_response(False, error='部门未找到'), 404

    @staticmethod
    def create_department(data):
        """创建部门信息"""

        # 校验部门编号是否存在并有效
        if 'code' not in data or not data['code'] or len(data['code'].strip()) < 2:
            return format_response(False, error='部门编号不能为空且至少为2个字符'), 400
        if Department.query.filter_by(code=data['code'].strip(), is_deleted=False).first():
            return format_response(False, error='部门编号已存在'), 400

        # 校验部门名称是否有效
        if 'name' not in data or not data['name'] or len(data['name'].strip()) < 2:
            return format_response(False, error='部门名称不能为空且至少为2个字符'), 400
        if not validate_department_name(data['name'].strip()):
            return format_response(False, error='部门名称只能包含中文字符、字母、数字和空格'), 400

        department = Department(
            code=data['code'].strip(),
            name=data['name'].strip(),
            description=data.get('description') or '',
            parent_id=data.get('parent_id') or None,
            is_deleted=False,
        )

        # 提交数据库更新
        try:
            db.session.add(department)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return format_response(False, error=f'数据库更新失败: {str(e)}'), 500

        return format_response(True, department.to_dict()), 200

    @staticmethod
    def update_department(department_id, data):
        """更新部门信息"""

        # 校验部门编号是否有效
        if 'code' not in data or not data['code'] or len(data['code'].strip()) < 2:
            return format_response(False, error='部门编号不能为空且至少为2个字符'), 400
        if Department.query.filter(Department.code == data['code'].strip(), Department.id != department_id,
                                   Department.is_deleted == False).first():
            return format_response(False, error='部门编号已存在'), 400

        # 校验部门名称是否有效
        if 'name' not in data or not data['name'] or len(data['name'].strip()) < 2:
            return format_response(False, error='部门名称不能为空且至少为2个字符'), 400
        if not validate_department_name(data['name'].strip()):
            return format_response(False, error='部门名称只能包含中文字符、字母、数字和空格'), 400

        # 查找现有的部门信息
        department = Department.query.filter_by(id=department_id, is_deleted=False).first()
        if not department:
            return format_response(False, error='部门未找到'), 404

        # 更新部门信息
        if 'code' in data:
            department.code = data['code'].strip()
        if 'name' in data:
            department.name = data['name'].strip()
        if 'description' in data:
            department.description = data.get('description') or ''
        if 'parent_id' in data:
            department.parent_id = data.get('parent_id') or None

        # 提交数据库更新
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return format_response(False, error=f'数据库更新失败: {str(e)}'), 500

        return format_response(True, department.to_dict()), 200

    @staticmethod
    def delete_department(department_id):
        """删除部门信息"""

        # 查找现有的部门信息
        department = Department.query.filter_by(id=department_id, is_deleted=False).first()

        if department:
            # 检查当前部门及其子部门是否有用户关联
            if department.has_children() or department.has_associated_users():
                return format_response(False, error='部门有关联数据无法删除'), 400

            department.is_deleted = True
            department.deleted_at = datetime.now()

            # 提交数据库更新
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return format_response(False, error=f'数据库更新失败: {str(e)}'), 500
            return format_response(True, {'message': '部门删除成功'}), 200

        return format_response(False, error='部门未找到'), 404

    @staticmethod
    def search_departments(json_string, page=1, per_page=10, sort_field='id', sort_order='asc'):
        """检索部门信息"""

        # 将参数中的json字符串转换成字典
        filters = {}
        if json_string:
            try:
                filters = json.loads(json_string)  # 将字符串转换为字典
            except ValueError:
                return format_response(False, error='无效的 JSON'), 400

        # 检查 sort_field 是否是 Department 模型中的有效列
        if sort_field not in Department.__table__.columns:
            return format_response(False, error='无效的排序字段'), 400

        # 创建查询对象
        query = Department.query.filter(Department.is_deleted == False)

        # 如果有部门编号的条件
        if filters.get('code'):
            query = query.filter(Department.name.contains(filters['code']))

        # 如果有部门名称的条件
        if filters.get('name'):
            query = query.filter(Department.name.contains(filters['name']))

        # 动态排序，确保sort_field是数据库表中的有效字段
        if sort_order.lower() == 'asc':
            query = query.order_by(asc(getattr(Department, sort_field)))
        elif sort_order.lower() == 'desc':
            query = query.order_by(desc(getattr(Department, sort_field)))
        else:
            # 如果排序顺序无效，则默认使用升序
            query = query.order_by(asc(getattr(Department, sort_field)))

        # 分页
        paginated_departments = query.paginate(page=page, per_page=per_page, error_out=False)

        # 返回分页后的数据、总页数、当前页和每页记录数
        return format_response(True, {
            "departments": [department.to_dict() for department in paginated_departments.items],
            "total_pages": paginated_departments.pages,
            "current_page": page,
            "per_page": per_page
        }), 200
