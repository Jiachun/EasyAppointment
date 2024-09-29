# -*- coding: utf-8 -*-
"""
# 文件名称: models/department.py
# 作者: 罗嘉淳
# 创建日期: 2024-09-29
# 版本: 1.0
# 描述: 部门模型文件。
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from extensions.db import db
from models import user_department


class Department(db.Model):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True)  # 部门ID
    name = Column(String(100), nullable=False, unique=True)  # 部门名称
    description = Column(String(255), nullable=True)  # 部门描述（可选）

    # 部门可以关联多个用户
    users = relationship('User', secondary=user_department, back_populates='departments')

    def __repr__(self):
        return f'<Role {self.name}>'