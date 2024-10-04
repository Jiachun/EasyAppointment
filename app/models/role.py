# -*- coding: utf-8 -*-
"""
# 文件名称: models/role.py
# 作者: 罗嘉淳
# 创建日期: 2024-09-29
# 版本: 1.0
# 描述: 角色模型文件。
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from extensions.db import db
from app.models import role_permission, user_role


# 角色模型
class Role(db.Model):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, autoincrement=True)  # 角色ID
    name = Column(String(50), unique=True, nullable=False)  # 角色名称

    # 角色可以拥有多个权限
    permissions = relationship('Permission', secondary=role_permission, back_populates='roles', lazy='dynamic')

    # 角色可以关联多个用户
    users = relationship('User', secondary=user_role, back_populates='roles', lazy='dynamic')

    def __repr__(self):
        return f'<Role {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    def is_associated(self):
        """检查角色是否被用户或权限关联"""
        return bool(self.permissions or self.users)
