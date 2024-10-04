# -*- coding: utf-8 -*-
"""
# 文件名称: controllers/permission_controller.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-04
# 版本: 1.0
# 描述: 权限信息逻辑控制器
"""

from app.models import Permission
from extensions.db import db


class PermissionController:
    @staticmethod
    def get_all_permissions(page=1, per_page=10):
        """获取所有权限信息"""

        # 分页
        paginated_permissions = Permission.query.paginate(page=page, per_page=per_page, error_out=False)

        # 返回分页后的数据、总页数、当前页和每页记录数
        return {
            "permissions": [permission.to_dict() for permission in paginated_permissions.items],
            "total_pages": paginated_permissions.pages,
            "current_page": page,
            "per_page": per_page
        }, 200


    @staticmethod
    def get_permission_by_id(permission_id):
        """根据ID获取权限信息"""
        permission = Permission.query.get(permission_id)
        if permission:
            return permission.to_dict(), 200
        return {'error': '权限未找到'}, 404


    @staticmethod
    def create_permission(data):
        """创建权限信息"""

        # 校验权限名称是否存在并有效
        if 'name' not in data or len(data['name']) < 3:
            return {'error': '权限名称不能为空且至少为3个字符'}, 400
        if Permission.query.filter_by(name=data['name']).first():
            return {'error': '权限名称已存在'}, 400

        permission = Permission(
            name=data['name'],
        )

        # 提交数据库更新
        try:
            db.session.add(permission)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': '数据库更新失败: {}'.format(str(e))}, 500

        return permission.to_dict(), 200


    @staticmethod
    def update_permission(permission_id, data):
        """更新权限信息"""

        # 校验权限名称是否有效
        if 'name' not in data or len(data['name']) < 3:
            return {'error': '权限名称不能为空且至少为3个字符'}, 400
        if Permission.query.filter(Permission.name==data['name'], Permission.id!=permission_id).first():
            return {'error': '权限名称已存在'}, 400

        # 查找现有的权限信息
        permission = Permission.query.get(permission_id)
        if not permission:
            return {'error': '权限未找到'}, 404

        # 更新权限信息
        if 'name' in data:
            permission.name = data['name']
        if 'description' in data:
            permission.description = data['description']

        # 提交数据库更新
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': '数据库更新失败: {}'.format(str(e))}, 500

        return permission.to_dict(), 200


    @staticmethod
    def delete_permission(permission_id):
        """删除权限信息"""

        # 查找现有的权限信息
        permission = Permission.query.get(permission_id)

        if permission:
            # 检查权限是否被用户或权限关联
            if permission.is_associated():
                return {'error': '权限有关联数据'}, 400

            # 提交数据库更新
            try:
                db.session.delete(permission)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return {'error': '数据库更新失败: {}'.format(str(e))}, 500
            return {'message': '权限删除成功'}, 200

        return {'error': '权限未找到'}, 404

