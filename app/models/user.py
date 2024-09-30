# -*- coding: utf-8 -*-
"""
# 文件名称: models/user.py
# 作者: 罗嘉淳
# 创建日期: 2024-09-29
# 版本: 1.0
# 描述: 用户模型文件。
"""

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from extensions.db import db
from app.models import user_role, user_department


# 用户模型
class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)  # 用户ID
    username = Column(String(50), unique=True, nullable=False)  # 用户名
    password_hash = Column(String(128), nullable=False)  # 密码
    first_name = Column(String(50), nullable=True)  # 名
    last_name = Column(String(50), nullable=True)  # 姓
    gender = Column(String(10), nullable=True)  # 性别
    id_type = Column(String(50), nullable=True)  # 证件类型
    id_number = Column(String(100), unique=True, nullable=True)  # 证件号码
    phone_number = Column(String(20), unique=True, nullable=False)  # 手机号码
    email = Column(String(120), unique=True, nullable=True)  #邮箱
    is_active = Column(Boolean, default=True)  # 是否激活
    is_staff = Column(Boolean, default=False)  # 是否工作人员

    # 用户可以拥有多个角色
    roles = relationship('Role', secondary=user_role, back_populates='users')

    # 用户可以拥有多个部门
    departments = relationship('Department', secondary=user_department, back_populates='users')

    def __repr__(self):
        return f'<User {self.username}>'

    def can(self, permission_name):
        """检查用户是否具有某个权限"""
        # 遍历用户的所有角色
        for role in self.roles:
            # 遍历角色的所有权限
            for perm in role.permissions:
                # 如果权限的名字和传入的 permission_name 匹配，返回 True
                if perm.name == permission_name:
                    return True
        # 如果遍历完所有角色和权限没有找到匹配的，返回 False
        return False





