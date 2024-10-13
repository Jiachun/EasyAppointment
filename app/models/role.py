# -*- coding: utf-8 -*-
"""
# 文件名称: models/role.py
# 作者: 罗嘉淳
# 创建日期: 2024-09-29
# 版本: 1.0
# 描述: 角色的模型文件。
"""

from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship

from extensions.db import db


# 角色模型
class Role(db.Model):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, autoincrement=True)  # 角色ID
    name = Column(String(50), nullable=False, index=True)  # 角色名称，唯一
    description = Column(String(255), nullable=True)  # 角色描述（可选）
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)  # 逻辑删除标记
    created_at = Column(DateTime, default=datetime.now, nullable=False)  # 创建时间，用于记录何时创建
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)  # 更新时间，用于记录何时更新
    deleted_at = Column(DateTime, nullable=True)  # 删除时间，用于记录何时删除

    # 定义反向关系
    user_roles = relationship('UserRole', back_populates='role', lazy='dynamic')
    role_permissions = relationship('RolePermission', back_populates='role', lazy='dynamic')

    def __repr__(self):
        return f'<Role {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }

    def is_associated(self):
        """检查角色是否被用户或权限关联"""
        # 检查是否有未被逻辑删除的用户关联
        if self.user_roles.filter_by(is_deleted=False).count() > 0:
            return True

        # 检查是否有未被逻辑删除的权限关联
        if self.role_permissions.filter_by(is_deleted=False).count() > 0:
            return True

        return False
