# -*- coding: utf-8 -*-
"""
# 文件名称: controllers/user_department_controller.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-04
# 版本: 1.0
# 描述: 用户部门关联逻辑控制器。
"""


from app.models import User, Department, UserDepartment
from extensions.db import db
from datetime import datetime


class UserDepartmentController:
    @staticmethod
    def get_departments_by_user(user_id):
        """获取用户的所有部门"""

        # 查找现有的用户信息
        user = User.query.filter_by(id=user_id, is_deleted=False).first()

        if not user:
            return {'error': '用户未找到'}, 404

        # 获取用户的所有部门，确保未被逻辑删除
        departments = []
        for user_department in user.user_departments.filter_by(is_deleted=False):
            department = user_department.department
            if not department.is_deleted:
                departments.append(department.to_dict())

        return {"departments": departments}, 200


    @staticmethod
    def add_department_to_user(user_id, department_id):
        """为用户添加部门"""

        if not department_id:
            return {'error': '部门ID不能为空'}, 400

        # 查找现有的用户和部门信息
        user = User.query.filter_by(id=user_id, is_deleted=False).first()
        department = Department.query.filter_by(id=department_id, is_deleted=False).first()

        if not user:
            return {'error': '用户未找到'}, 404
        if not department:
            return {'error': '部门不存在'}, 404

        # 检查是否已经关联
        existing_relation = UserDepartment.query.filter_by(user_id=user.id, department_id=department.id, is_deleted=False).first()

        if existing_relation:
            return {'error': '该用户已关联此部门'}, 400

        # 添加新的用户-部门关联
        new_relation = UserDepartment(user_id=user.id, department_id=department.id)

        # 提交数据库更新
        try:
            db.session.add(new_relation)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': '数据库更新失败: {}'.format(str(e))}, 500

        return {'message': '用户已成功添加到此部门'}, 200


    @staticmethod
    def remove_department_from_user(user_id, department_id):
        """从用户中移除部门"""

        if not department_id:
            return {'error': '部门ID不能为空'}, 400

        # 查找现有的用户和部门信息
        user = User.query.filter_by(id=user_id, is_deleted=False).first()
        department = Department.query.filter_by(id=department_id, is_deleted=False).first()

        if not user:
            return {'error': '用户未找到'}, 404
        if not department:
            return {'error': '部门不存在'}, 404

        # 查找现有的关联记录
        relation = UserDepartment.query.filter_by(user_id=user.id, department_id=department.id, is_deleted=False).first()

        if not relation:
            return {'error': '用户未关联此部门'}, 404

        # 执行逻辑删除
        relation.is_deleted = True
        relation.deleted_at = datetime.now()

        # 提交数据库更新
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': '数据库更新失败: {}'.format(str(e))}, 500

        return {'message': '用户已成功从部门中移除'}, 200
