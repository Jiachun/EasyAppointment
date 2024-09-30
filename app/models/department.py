# -*- coding: utf-8 -*-
"""
# 文件名称: models/department.py
# 作者: 罗嘉淳
# 创建日期: 2024-09-29
# 版本: 1.0
# 描述: 部门模型文件。
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from extensions.db import db
from app.models import user_department


class Department(db.Model):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, autoincrement=True)  # 部门ID
    code = Column(db.String(50), nullable=False, unique=True)  # 部门编号，唯一
    name = Column(String(100), nullable=False)  # 部门名称
    description = Column(String(255), nullable=True)  # 部门描述（可选）
    parent_id = Column(Integer, ForeignKey('departments.id'), nullable=True)  # 上级部门ID

    # 部门可以关联多个用户
    users = relationship('User', secondary=user_department, back_populates='departments')

    # 自引用关系，parent 指向上级部门
    parent = relationship(
        'Department',
        remote_side=[Column('id')],
        back_populates = 'children',
        lazy='select'  # 使用懒加载，默认值 'select'
    )

    # children 指向所有下级部门
    children = relationship(
        'Department',
        back_populates = 'parent',
        lazy='dynamic',  # 动态加载，适合处理大规模一对多关系
        cascade='all, delete-orphan'  # 当父部门删除时，级联删除子部门
    )

    def __repr__(self):
        return f'<Role {self.name}>'

    def get_ancestors(self):
        ancestors = []
        department = self
        while department.parent is not None:
            ancestors.append(department.parent)
            department = department.parent
        return ancestors