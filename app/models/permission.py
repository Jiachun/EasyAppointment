# -*- coding: utf-8 -*-
"""
# 文件名称: models/permission.py
# 作者: 罗嘉淳
# 创建日期: 2024-09-29
# 版本: 1.0
# 描述: 权限模型文件。
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from extensions.db import db
from app.models import role_permission


# 权限模型
class Permission(db.Model):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True, autoincrement=True)  # 权限ID
    name = Column(String(50), unique=True, nullable=False)  # 权限名称
    description = Column(String(255))  # 权限描述（可选）

    # 权限可以关联多个角色
    roles = relationship('Role', secondary=role_permission, back_populates='permissions')

    def __repr__(self):
        return f'<Permission {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

    def is_associated(self):
        """检查权限是否被角色关联"""
        return bool(self.roles)