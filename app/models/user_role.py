# -*- coding: utf-8 -*-
"""
# 文件名称: models/user_role.py
# 作者: 罗嘉淳
# 创建日期: 2024-09-29
# 版本: 1.0
# 描述: 用户角色关联模型文件。
"""

from sqlalchemy import Column, Integer, ForeignKey, Table
from extensions.db import db


# 用户和角色的多对多关系表
user_role = Table('user_role', db.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
)