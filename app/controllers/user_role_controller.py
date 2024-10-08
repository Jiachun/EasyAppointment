# -*- coding: utf-8 -*-
"""
# 文件名称: controllers/user_role_controller.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-04
# 版本: 1.0
# 描述: 用户角色关联逻辑控制器。
"""

from app.models import User, Role
from extensions.db import db

class UserRoleController:
    @staticmethod
    def get_roles_by_user(user_id):
        """获取用户的所有角色"""

        # 查找现有的用户信息
        user = User.query.filter_by(id=user_id, is_deleted=False).first()

        if not user:
            return {'error': '用户未找到'}, 404

        return {"roles": [role.to_dict() for role in user.roles]}, 200


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

        # 校验用户是否已经拥有该角色
        if role in user.roles:
            return {'error': '该用户已拥有该角色'}, 404

        user.roles.append(role)

        # 提交数据库更新
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': '数据库更新失败: {}'.format(str(e))}, 500

        return {"roles": [role.to_dict() for role in user.roles]}, 200


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

        # 校验用户是否已经拥有该角色
        if role not in user.roles:
            return {'error': '该用户没有该角色'}, 404

        user.roles.remove(role)

        # 提交数据库更新
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': '数据库更新失败: {}'.format(str(e))}, 500

        return {"roles": [role.to_dict() for role in user.roles]}, 200
