# -*- coding: utf-8 -*-
"""
# 文件名称: models/user_department.py
# 作者: 罗嘉淳
# 创建日期: 2024-09-29
# 版本: 1.0
# 描述: 用户部门关联模型文件。
"""

from sqlalchemy import Column, Integer, ForeignKey, Table
from extensions.db import db


# 用户和部门的多对多关系表
user_department = Table('user_department', db.Model.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('department_id', Integer, ForeignKey('departments.id'), primary_key=True)
)