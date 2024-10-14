# -*- coding: utf-8 -*-
"""
# 文件名称: controllers/user_role_controller.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-04
# 版本: 1.0
# 描述: 用户和角色关联的逻辑控制器。
"""

from datetime import datetime

from app.models import User, Role, UserRole
from extensions.db import db
from utils.format_utils import format_response


class UserRoleController:
    @staticmethod
    def get_roles_by_user(user_id):
        """获取用户的所有角色"""

        # 查找现有的用户信息
        user = User.query.filter_by(id=user_id, is_deleted=False).first()

        if not user:
            return format_response(False, error='用户未找到'), 404

        # 获取用户的所有角色，确保未被逻辑删除
        roles = []
        for user_role in user.user_roles.filter_by(is_deleted=False):
            role = user_role.role
            if not role.is_deleted:
                roles.append(role.to_dict())

        return format_response(True, {"roles": roles}), 200

    @staticmethod
    def add_roles_to_user(user_id, role_ids):
        """为用户添加角色"""

        if not role_ids:
            return format_response(False, error='角色ID列表不能为空'), 400

        # 查找现有的用户信息
        user = User.query.filter_by(id=user_id, is_deleted=False).first()

        if not user:
            return format_response(False, error='用户不存在'), 404

        # 获取所有新的角色
        roles = Role.query.filter(Role.id.in_(role_ids), Role.is_deleted == False).all()

        if not roles:
            return format_response(False, error='角色不存在或无效'), 404

        # 遍历每个角色，确保角色未与该用户关联
        for role in roles:
            existing_relation = UserRole.query.filter_by(user_id=user.id, role_id=role.id,
                                                         is_deleted=False).first()

            if existing_relation:
                continue  # 角色已经关联，跳过

            # 创建新的用户-角色关联
            new_user_role = UserRole(user_id=user.id, role_id=role.id)
            db.session.add(new_user_role)

        # 提交数据库更新
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return format_response(False, error=f'数据库更新失败: {str(e)}'), 500

        return format_response(True, {'message': '角色已成功添加到用户'}), 200

    @staticmethod
    def remove_roles_from_user(user_id, role_ids):
        """从用户中移除角色"""

        if not role_ids:
            return format_response(False, error='角色ID列表不能为空'), 400

        # 查找现有的用户信息
        user = User.query.filter_by(id=user_id, is_deleted=False).first()

        if not user:
            return format_response(False, error='用户不存在'), 404

        # 查找现有的角色信息
        roles = Role.query.filter(Role.id.in_(role_ids), Role.is_deleted == False).all()

        if not roles:
            return format_response(False, error='角色不存在或无效'), 404

        # 遍历每个角色，检查其是否已与该用户关联
        for role in roles:
            existing_relation = UserRole.query.filter_by(user_id=user.id, role_id=role.id,
                                                         is_deleted=False).first()

            if not existing_relation:
                continue  # 如果没有找到有效的关联关系，跳过

            # 执行逻辑删除操作
            existing_relation.is_deleted = True
            existing_relation.deleted_at = datetime.now()

        # 提交数据库更新
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return format_response(False, error=f'数据库更新失败: {str(e)}'), 500

        return format_response(True, {'message': '角色已成功从用户中移除'}), 200
