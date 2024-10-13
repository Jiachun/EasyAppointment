# -*- coding: utf-8 -*-
"""
# 文件名称: models/role_permission.py
# 作者: 罗嘉淳
# 创建日期: 2024-09-29
# 版本: 1.0
# 描述: 角色和权限关联的模型文件。
"""

from datetime import datetime

from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from extensions.db import db


# 角色和权限的关联模型
class RolePermission(db.Model):
    __tablename__ = 'role_permission'

    id = Column(Integer, primary_key=True, autoincrement=True)  # 为关联模型创建主键
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False, index=True)  # 关联的角色ID
    permission_id = Column(Integer, ForeignKey('permissions.id'), nullable=False, index=True)  # 关联的权限ID
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)  # 逻辑删除标记
    created_at = Column(DateTime, default=datetime.now, nullable=False)  # 创建时间，用于记录何时创建
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)  # 更新时间，用于记录何时更新
    deleted_at = Column(DateTime, nullable=True)  # 删除时间，用于记录何时删除

    # 定义反向关系
    role = relationship('Role', back_populates='role_permissions')
    permission = relationship('Permission', back_populates='role_permissions')
