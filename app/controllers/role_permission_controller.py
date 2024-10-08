# -*- coding: utf-8 -*-
"""
# 文件名称: controllers/role_permission_controller.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-04
# 版本: 1.0
# 描述: 角色权限关联逻辑控制器。
"""

from app.models import Role, Permission
from extensions.db import db

class RolePermissionController:
    @staticmethod
    def get_permissions_by_role(role_id):
        """获取角色的所有权限"""

        # 查找现有的角色信息
        role = Role.query.filter_by(id=role_id, is_deleted=False).first()

        if not role:
            return {'error': '角色不存在'}, 404

        return {"permissions": [permission.to_dict() for permission in role.permissions]}, 200


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

        role.permissions.extend(permissions)

        # 提交数据库更新
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': '数据库更新失败: {}'.format(str(e))}, 500

        return {"permissions": [permission.to_dict() for permission in role.permissions]}, 200


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

        # 如果权限存在于角色中，移除关联
        for permission in permissions:
            if permission in role.permissions:
                role.permissions.remove(permission)

        # 提交数据库更新
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': '数据库更新失败: {}'.format(str(e))}, 500

        return {"permissions": [permission.to_dict() for permission in role.permissions]}, 200
