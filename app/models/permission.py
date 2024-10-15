# -*- coding: utf-8 -*-
"""
# 文件名称: models/permission.py
# 作者: 罗嘉淳
# 创建日期: 2024-09-29
# 版本: 1.0
# 描述: 权限的模型文件。
"""

from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship

from extensions.db import db


# 权限模型
class Permission(db.Model):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True, autoincrement=True)  # 权限ID
    name = Column(String(50), nullable=False, index=True)  # 权限名称，唯一
    type = Column(String(20), nullable=False, index=True)  # 权限类型
    description = Column(String(255), nullable=True)  # 权限描述（可选）
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)  # 逻辑删除标记
    created_at = Column(DateTime, default=datetime.now, nullable=False)  # 创建时间，用于记录何时创建
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)  # 更新时间，用于记录何时更新
    deleted_at = Column(DateTime, nullable=True)  # 删除时间，用于记录何时删除

    # 定义反向关系
    role_permissions = relationship('RolePermission', back_populates='permission', lazy='dynamic')

    def __repr__(self):
        return f'<Permission {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'description': self.description,
        }

    def is_associated(self):
        """检查权限是否被角色关联（排除逻辑删除的关联）"""
        return self.role_permissions.filter_by(is_deleted=False).count() > 0  # 只计算未被逻辑删除的关联
