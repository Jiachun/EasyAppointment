# -*- coding: utf-8 -*-
"""
# 文件名称: controllers/role_permission_controller.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-04
# 版本: 1.0
# 描述: 角色权限关联逻辑控制器。
"""


from app.models import Role, Permission, RolePermission
from extensions.db import db
from datetime import datetime


class RolePermissionController:
    @staticmethod
    def get_permissions_by_role(role_id):
        """获取角色的所有权限"""

        # 查找现有的角色信息
        role = Role.query.filter_by(id=role_id, is_deleted=False).first()

        if not role:
            return {'error': '角色不存在'}, 404

        # 获取角色关联的权限，确保权限和关联表都未被逻辑删除
        permissions = []
        for role_permission in role.role_permissions.filter_by(is_deleted=False):
            permission = role_permission.permission
            if not permission.is_deleted:
                permissions.append(permission.to_dict())

        return {"permissions": permissions}, 200


    @staticmethod
    def add_permissions_to_role(role_id, permission_ids):
        """为角色添加权限"""

        if not permission_ids:
            return {'error': '权限ID列表不能为空'}, 400

        # 查找现有的角色信息
        role = Role.query.filter_by(id=role_id, is_deleted=False).first()

        if not role:
            return {'error': '角色不存在'}, 404

        # 获取所有新的权限
        permissions = Permission.query.filter(Permission.id.in_(permission_ids), Permission.is_deleted==False).all()

        if not permissions:
            return {'error': '权限不存在或无效'}, 404

        # 遍历每个权限，确保权限未与该角色关联
        for permission in permissions:
            existing_relation = RolePermission.query.filter_by(role_id=role.id, permission_id=permission.id, is_deleted=False).first()

            if existing_relation:
                continue  # 权限已经关联，跳过

            # 创建新的角色-权限关联
            new_role_permission = RolePermission(role_id=role.id, permission_id=permission.id)
            db.session.add(new_role_permission)

        # 提交数据库更新
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': '数据库更新失败: {}'.format(str(e))}, 500

        return {'message': '权限已成功添加到角色'}, 200


    @staticmethod
    def remove_permissions_from_role(role_id, permission_ids):
        """从角色中移除权限"""

        if not permission_ids:
            return {'error': '权限ID列表不能为空'}, 400

        # 查找现有的角色信息
        role = Role.query.filter_by(id=role_id, is_deleted=False).first()

        if not role:
            return {'error': '角色不存在'}, 404

        # 查找现有的权限信息
        permissions = Permission.query.filter(Permission.id.in_(permission_ids), Permission.is_deleted==False).all()

        if not permissions:
            return {'error': '权限不存在或无效'}, 404

        # 遍历每个权限，检查其是否已与该角色关联
        for permission in permissions:
            existing_relation = RolePermission.query.filter_by(role_id=role.id, permission_id=permission.id, is_deleted=False).first()

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
            return {'error': '数据库更新失败: {}'.format(str(e))}, 500

        return {'message': '权限已成功从角色中移除'}, 200
