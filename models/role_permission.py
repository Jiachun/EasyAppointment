# -*- coding: utf-8 -*-
"""
# 文件名称: models/role_permission.py
# 作者: 罗嘉淳
# 创建日期: 2024-09-29
# 版本: 1.0
# 描述: 角色权限关联模型文件。
"""

from sqlalchemy import Column, Integer, ForeignKey, Table
from extensions.db import db


# 角色和权限的多对多关系表
role_permission = Table('role_permission', db.Model.metadata,
    Column('role_id', Integer, ForeignKey('roles.id')),
    Column('permission_id', Integer, ForeignKey('permissions.id'))
)