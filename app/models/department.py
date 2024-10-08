# -*- coding: utf-8 -*-
"""
# 文件名称: models/department.py
# 作者: 罗嘉淳
# 创建日期: 2024-09-29
# 版本: 1.0
# 描述: 部门模型文件。
"""


from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from extensions.db import db
from datetime import datetime


class Department(db.Model):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, autoincrement=True)  # 部门ID
    code = Column(db.String(20), nullable=False, index=True)  # 部门编号，唯一
    name = Column(String(50), nullable=False, index=True)  # 部门名称
    description = Column(String(255), nullable=True)  # 部门描述（可选）
    parent_id = Column(Integer, ForeignKey('departments.id'), nullable=True, index=True)  # 上级部门ID
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)  # 逻辑删除标记
    created_at = Column(DateTime, default=datetime.now(), nullable=False)  # 创建时间，用于记录何时创建
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)  # 更新时间，用于记录何时更新
    deleted_at = Column(DateTime, nullable=True)  # 删除时间，用于记录何时删除

    # 定义反向关系
    user_departments = relationship('UserDepartment', back_populates='department', lazy='dynamic')

    # 自引用关系，parent 指向上级部门
    # noinspection PyTypeChecker
    parent = relationship(
        'Department',
        remote_side=[id],
        back_populates = 'children',
        lazy='select'  # 使用懒加载，默认值 'select'
    )

    # children 指向所有下级部门
    children = relationship(
        'Department',
        back_populates = 'parent',
        lazy='dynamic',  # 动态加载，适合处理大规模一对多关系
    )

    def __repr__(self):
        return f'<Department {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'description': self.description,
            'parent_id': self.parent_id,
        }

    def has_children(self):
        """检查当前部门是否有子部门，排除已逻辑删除的子部门"""
        return self.children.filter_by(is_deleted=False).count() > 0

    def has_associated_users(self):
        """检查当前部门或子部门是否有关联的用户，排除已逻辑删除的用户和部门"""
        # 检查当前部门是否有关联的用户
        if self.user_departments.filter_by(is_deleted=False).count() > 0:
            return True

        # 检查子部门是否有关联的用户
        for child in self.children.filter_by(is_deleted=False):
            if child.has_associated_users():
                return True

        return False