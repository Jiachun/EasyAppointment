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
from datetime import datetime
from sqlalchemy import asc, desc
import json


class PermissionController:
    @staticmethod
    def get_all_permissions(page=1, per_page=10):
        """获取所有权限信息"""

        # 分页
        paginated_permissions = Permission.query.filter_by(is_deleted=False).paginate(page=page, per_page=per_page, error_out=False)

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
        permission = Permission.query.filter_by(id=permission_id, is_deleted=False).first()
        if permission:
            return permission.to_dict(), 200
        return {'error': '权限未找到'}, 404


    @staticmethod
    def create_permission(data):
        """创建权限信息"""

        # 校验权限名称是否存在并有效
        if 'name' not in data or not data['name'] or len(data['name']) < 3:
            return {'error': '权限名称不能为空且至少为3个字符'}, 400
        if Permission.query.filter_by(name=data['name'], is_deleted=False).first():
            return {'error': '权限名称已存在'}, 400

        permission = Permission(
            name=data['name'],
            description=data.get('description') or '',
            is_deleted=False,
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
        if 'name' not in data or not data['name'] or len(data['name']) < 3:
            return {'error': '权限名称不能为空且至少为3个字符'}, 400
        if Permission.query.filter(Permission.name==data['name'], Permission.id!=permission_id, Permission.is_deleted==False).first():
            return {'error': '权限名称已存在'}, 400

        # 查找现有的权限信息
        permission = Permission.query.filter_by(id=permission_id, is_deleted=False).first()
        if not permission:
            return {'error': '权限未找到'}, 404

        # 更新权限信息
        if 'name' in data:
            permission.name = data['name']
        if 'description' in data:
            permission.description = data.get('description') or '',

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
        permission = Permission.query.filter_by(id=permission_id, is_deleted=False).first()

        if permission:
            # 检查权限是否被用户或权限关联
            if permission.is_associated():
                return {'error': '权限有关联数据无法删除'}, 400

            permission.is_deleted = True
            permission.deleted_at = datetime.now()

            # 提交数据库更新
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return {'error': '数据库更新失败: {}'.format(str(e))}, 500
            return {'message': '权限删除成功'}, 200

        return {'error': '权限未找到'}, 404


    @staticmethod
    def search_permissions(json_string, page=1, per_page=10, sort_field='id', sort_order='asc'):
        """检索权限信息"""

        # 将参数中的json字符串转换成字典
        filters = {}
        if json_string:
            try:
                filters = json.loads(json_string)  # 将字符串转换为字典
            except ValueError:
                return {"error": "无效的 JSON"}, 400

        # 检查 sort_field 是否是 Permission 模型中的有效列
        if sort_field not in Permission.__table__.columns:
            return {'error': '无效的排序字段'}, 400

        # 创建查询对象
        query = Permission.query.filter(Permission.is_deleted==False)

        # 如果有角色名称的条件
        if filters.get('name'):
            query = query.filter(Permission.name.contains(filters['name']))

        # 动态排序，确保sort_field是数据库表中的有效字段
        if sort_order.lower() == 'asc':
            query = query.order_by(asc(getattr(Permission, sort_field)))
        elif sort_order.lower() == 'desc':
            query = query.order_by(desc(getattr(Permission, sort_field)))
        else:
            # 如果排序顺序无效，则默认使用升序
            query = query.order_by(asc(getattr(Permission, sort_field)))

        # 分页
        paginated_permissions = query.paginate(page=page, per_page=per_page, error_out=False)

        # 返回分页后的数据、总页数、当前页和每页记录数
        return {
            "permissions": [permission.to_dict() for permission in paginated_permissions.items],
            "total_pages": paginated_permissions.pages,
            "current_page": page,
            "per_page": per_page
        }, 200