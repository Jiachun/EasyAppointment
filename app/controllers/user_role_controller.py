# -*- coding: utf-8 -*-
"""
# 文件名称: controllers/user_role_controller.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-04
# 版本: 1.0
# 描述: 用户角色关联逻辑控制器。
"""


from app.models import User, Role, UserRole
from extensions.db import db
from datetime import datetime


class UserRoleController:
    @staticmethod
    def get_roles_by_user(user_id):
        """获取用户的所有角色"""

        # 查找现有的用户信息
        user = User.query.filter_by(id=user_id, is_deleted=False).first()

        if not user:
            return {'error': '用户未找到'}, 404

        # 获取用户的所有角色，确保未被逻辑删除
        roles = []
        for user_role in user.user_roles.filter_by(is_deleted=False):
            role = user_role.role
            if not role.is_deleted:
                roles.append(role.to_dict())

        return {"roles": roles}, 200


    @staticmethod
    def add_role_to_user(user_id, role_id):
        """为用户添加角色"""

        if not role_id:
            return {'error': '角色ID不能为空'}, 400

        # 查找现有的用户和角色信息
        user = User.query.filter_by(id=user_id, is_deleted=False).first()
        role = Role.query.filter_by(id=role_id, is_deleted=False).first()

        if not user:
            return {'error': '用户未找到'}, 404
        if not role:
            return {'error': '角色不存在'}, 404

        # 检查是否已经关联
        existing_relation = UserRole.query.filter_by(user_id=user.id, role_id=role.id, is_deleted=False).first()

        if existing_relation:
            return {'error': '该用户已关联此角色'}, 400

        # 添加新的用户-角色关联
        new_relation = UserRole(user_id=user.id, role_id=role.id)

        # 提交数据库更新
        try:
            db.session.add(new_relation)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': '数据库更新失败: {}'.format(str(e))}, 500

        return {'message': '用户已成功添加到此角色'}, 200


    @staticmethod
    def remove_role_from_user(user_id, role_id):
        """从用户中移除角色"""

        if not role_id:
            return {'error': '角色ID不能为空'}, 400

        # 查找现有的用户和角色信息
        user = User.query.filter_by(id=user_id, is_deleted=False).first()
        role = Role.query.filter_by(id=role_id, is_deleted=False).first()

        if not user:
            return {'error': '用户未找到'}, 404
        if not role:
            return {'error': '角色不存在'}, 404

        # 查找现有的关联记录
        relation = UserRole.query.filter_by(user_id=user.id, role_id=role.id, is_deleted=False).first()

        if not relation:
            return {'error': '用户未关联此角色'}, 404

        # 执行逻辑删除
        relation.is_deleted = True
        relation.deleted_at = datetime.now()

        # 提交数据库更新
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': '数据库更新失败: {}'.format(str(e))}, 500

        return {'message': '用户已成功从角色中移除'}, 200
