# -*- coding: utf-8 -*-
"""
# 文件名称: controllers/department_controller.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-04
# 版本: 1.0
# 描述: 部门信息逻辑控制器
"""

from app.models import Department
from extensions.db import db


class DepartmentController:
    @staticmethod
    def get_all_departments(page=1, per_page=10):
        """获取所有部门信息"""

        # 分页
        paginated_departments = Department.query.paginate(page=page, per_page=per_page, error_out=False)

        # 返回分页后的数据、总页数、当前页和每页记录数
        return {
            "departments": [department.to_dict() for department in paginated_departments.items],
            "total_pages": paginated_departments.pages,
            "current_page": page,
            "per_page": per_page
        }, 200


    @staticmethod
    def get_department_by_id(department_id):
        """根据ID获取部门信息"""
        department = Department.query.get(department_id)
        if department:
            return department.to_dict(), 200
        return {'error': '部门未找到'}, 404


    @staticmethod
    def create_department(data):
        """创建部门信息"""

        # 校验部门编号是否存在并有效
        if 'code' not in data or len(data['code']) < 2:
            return {'error': '部门编号不能为空且至少为2个字符'}, 400
        if Department.query.filter_by(code=data['code']).first():
            return {'error': '部门编号已存在'}, 400

        # 校验部门名称是否有效
        if 'name' not in data or len(data['name']) < 2:
            return {'error': '部门名称不能为空且至少为2个字符'}, 400

        department = Department(
            code=data['code'],
            name=data['name'],
            description=data.get('description', ''),
            parent_id=data.get('parent_id', None),
        )

        # 提交数据库更新
        try:
            db.session.add(department)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': '数据库更新失败: {}'.format(str(e))}, 500

        return department.to_dict(), 200


    @staticmethod
    def update_department(department_id, data):
        """更新部门信息"""

        # 校验部门编号是否有效
        if 'code' not in data or len(data['code']) < 2:
            return {'error': '部门编号不能为空且至少为2个字符'}, 400
        if Department.query.filter(Department.code==data['code'], Department.id!=department_id).first():
            return {'error': '部门编号已存在'}, 400

        # 校验部门名称是否有效
        if 'name' not in data or len(data['name']) < 2:
            return {'error': '部门名称不能为空且至少为2个字符'}, 400

        # 查找现有的部门信息
        department = Department.query.get(department_id)
        if not department:
            return {'error': '部门未找到'}, 404

        # 更新部门信息
        if 'code' in data:
            department.code = data['code']
        if 'name' in data:
            department.name = data['name']
        if 'description' in data:
            department.description = data['description']
        if 'parent_id' in data:
            department.parent_id = data['parent_id']

        # 提交数据库更新
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': '数据库更新失败: {}'.format(str(e))}, 500

        return department.to_dict(), 200


    @staticmethod
    def delete_department(department_id):
        """删除部门信息"""

        # 查找现有的部门信息
        department = Department.query.get(department_id)

        if department:
            # 检查当前部门及其子部门是否有用户关联
            if department.has_associated_users():
                return {'error': '部门有关联数据'}, 400

            # 提交数据库更新
            try:
                db.session.delete(department)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return {'error': '数据库更新失败: {}'.format(str(e))}, 500
            return {'message': '部门删除成功'}, 200

        return {'error': '部门未找到'}, 404

