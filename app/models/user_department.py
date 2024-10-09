# -*- coding: utf-8 -*-
"""
# 文件名称: models/user_department.py
# 作者: 罗嘉淳
# 创建日期: 2024-09-29
# 版本: 1.0
# 描述: 用户部门关联模型文件。
"""

from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from extensions.db import db
from datetime import datetime


# 用户和部门的关联模型
class UserDepartment(db.Model):
    __tablename__ = 'user_department'

    id = Column(Integer, primary_key=True, autoincrement=True)  # 为关联模型创建主键
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)  # 关联的用户ID
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False, index=True)  # 关联的部门ID
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)  # 逻辑删除标记
    created_at = Column(DateTime, default=datetime.now, nullable=False)  # 创建时间，用于记录何时创建
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)  # 更新时间，用于记录何时更新
    deleted_at = Column(DateTime, nullable=True)  # 删除时间，用于记录何时删除

    # 定义反向关系
    user = relationship('User', back_populates='user_departments')
    department = relationship('Department', back_populates='user_departments')