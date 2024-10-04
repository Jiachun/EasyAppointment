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
        role = Role.query.get(role_id)

        if not role:
            return {'error': '角色不存在'}, 404

        return {"permissions": [permission.to_dict() for permission in role.permissions]}, 200

    @staticmethod
    def assign_permission_to_role(role_id, permission_id):
        """为角色分配权限"""

        # 查找现有的角色信息
        role = Role.query.get(role_id)

        # 查找现有的权限信息
        permission = Permission.query.get(permission_id)

        if not role:
            return {'error': '角色不存在'}, 404
        if not permission:
            return {'error': '权限不存在'}, 404

        # 如果权限未分配给角色，添加关联
        if permission not in role.permissions:
            role.permissions.append(permission)

            # 提交数据库更新
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return {'error': '数据库更新失败: {}'.format(str(e))}, 500
            return {'message': '权限分配成功'}, 200

        return {'error': '该权限已分配给角色'}, 400

    @staticmethod
    def remove_permission_from_role(role_id, permission_id):
        """从角色中移除权限"""

        # 查找现有的角色信息
        role = Role.query.get(role_id)

        # 查找现有的权限信息
        permission = Permission.query.get(permission_id)

        if not role:
            return {'error': '角色不存在'}, 404
        if not permission:
            return {'error': '权限不存在'}, 404

        # 如果权限存在于角色中，移除关联
        if permission in role.permissions:
            role.permissions.remove(permission)

            # 提交数据库更新
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return {'error': '数据库更新失败: {}'.format(str(e))}, 500
            return {'message': '权限移除成功'}, 200

        return {'error': '该角色不具备此权限'}, 400

    @staticmethod
    def update_permissions_for_role(role_id, permission_ids):
        """更新角色的权限列表"""

        # 查找现有的角色信息
        role = Role.query.get(role_id)

        if not role:
            return {'error': '角色不存在'}, 404

        # 获取所有新的权限
        permissions = Permission.query.filter(Permission.id.in_(permission_ids)).all()

        # 更新角色的权限
        role.permissions = permissions

        # 提交数据库更新
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': '数据库更新失败: {}'.format(str(e))}, 500

        return {'message': '权限更新成功'}, 200