# -*- coding: utf-8 -*-
"""
# 文件名称: controllers/user_department_controller.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-04
# 版本: 1.0
# 描述: 用户部门关联逻辑控制器。
"""

from app.models import User, Department
from extensions.db import db

class UserDepartmentController:
    @staticmethod
    def get_departments_by_user(user_id):
        """获取用户的所有部门"""

        # 查找现有的用户信息
        user = User.query.filter_by(id=user_id, is_deleted=False).first()

        if not user:
            return {'error': '用户未找到'}, 404

        return {"departments": [department.to_dict() for department in user.departments]}, 200


    @staticmethod
    def add_department_to_user(user_id, department_id):
        """为用户添加部门"""

        if not department_id:
            return {'error': '部门ID不能为空'}, 400

        # 查找现有的用户和部门信息
        user = User.query.filter_by(id=user_id, is_deleted=False).first()
        department = Department.query.get(department_id)

        if not user:
            return {'error': '用户未找到'}, 404
        if not department:
            return {'error': '部门不存在'}, 404

        # 校验用户是否已经拥有该部门
        if department in user.departments:
            return {'error': '该用户已属于该部门'}, 404

        user.departments.append(department)

        # 提交数据库更新
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': '数据库更新失败: {}'.format(str(e))}, 500

        return {"departments": [department.to_dict() for department in user.departments]}, 200


    @staticmethod
    def remove_department_from_user(user_id, department_id):
        """从用户中移除部门"""

        if not department_id:
            return {'error': '部门ID不能为空'}, 400

        # 查找现有的用户和部门信息
        user = User.query.filter_by(id=user_id, is_deleted=False).first()
        department = Department.query.get(department_id)

        if not user:
            return {'error': '用户未找到'}, 404
        if not department:
            return {'error': '部门不存在'}, 404

        # 校验用户是否已经拥有该部门
        if department not in user.departments:
            return {'error': '该用户不属于该部门'}, 404

        user.departments.remove(department)

        # 提交数据库更新
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': '数据库更新失败: {}'.format(str(e))}, 500

        return {"departments": [department.to_dict() for department in user.departments]}, 200
