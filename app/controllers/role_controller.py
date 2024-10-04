# -*- coding: utf-8 -*-
"""
# 文件名称: controllers/role_controller.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-04
# 版本: 1.0
# 描述: 角色信息逻辑控制器
"""

from app.models import Role
from extensions.db import db


class RoleController:
    @staticmethod
    def get_all_roles(page=1, per_page=10):
        """获取所有角色信息"""

        # 分页
        paginated_roles = Role.query.paginate(page=page, per_page=per_page, error_out=False)

        # 返回分页后的数据、总页数、当前页和每页记录数
        return {
            "roles": [role.to_dict() for role in paginated_roles.items],
            "total_pages": paginated_roles.pages,
            "current_page": page,
            "per_page": per_page
        }, 200


    @staticmethod
    def get_role_by_id(role_id):
        """根据ID获取角色信息"""
        role = Role.query.get(role_id)
        if role:
            return role.to_dict(), 200
        return {'error': '角色未找到'}, 404


    @staticmethod
    def create_role(data):
        """创建角色信息"""

        # 校验角色名称是否存在并有效
        if 'name' not in data or len(data['name']) < 3:
            return {'error': '角色名称不能为空且至少为3个字符'}, 400
        if Role.query.filter_by(name=data['name']).first():
            return {'error': '角色名称已存在'}, 400

        role = Role(
            name=data['name'],
        )

        # 提交数据库更新
        try:
            db.session.add(role)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': '数据库更新失败: {}'.format(str(e))}, 500

        return role.to_dict(), 200


    @staticmethod
    def update_role(role_id, data):
        """更新角色信息"""

        # 校验角色名称是否有效
        if 'name' not in data or len(data['name']) < 3:
            return {'error': '角色名称不能为空且至少为3个字符'}, 400
        if Role.query.filter(Role.name==data['name'], Role.id!=role_id).first():
            return {'error': '角色名称已存在'}, 400

        # 查找现有的角色信息
        role = Role.query.get(role_id)
        if not role:
            return {'error': '角色未找到'}, 404

        # 更新角色信息
        if 'name' in data:
            role.name = data['name']

        # 提交数据库更新
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': '数据库更新失败: {}'.format(str(e))}, 500

        return role.to_dict(), 200


    @staticmethod
    def delete_role(role_id):
        """删除角色信息"""

        # 查找现有的角色信息
        role = Role.query.get(role_id)

        if role:
            # 检查角色是否被用户或权限关联
            if role.is_associated():
                return {'error': '角色有关联数据'}, 400

            # 提交数据库更新
            try:
                db.session.delete(role)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return {'error': '数据库更新失败: {}'.format(str(e))}, 500
            return {'message': '角色删除成功'}, 200

        return {'error': '角色未找到'}, 404

