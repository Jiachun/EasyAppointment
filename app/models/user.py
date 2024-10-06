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
from .user_role import user_role
from .user_department import user_department


# 用户模型
class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)  # 用户ID
    username = Column(String(50), nullable=False)  # 用户名
    password_hash = Column(String(128), nullable=False)  # 密码
    phone_number = Column(String(20), nullable=False)  # 手机号码
    openid = Column(String(128), nullable=True)  # OpenID
    name = Column(String(50), nullable=True)  # 姓名
    gender = Column(String(10), nullable=True)  # 性别
    id_type = Column(String(50), nullable=True)  # 证件类型
    id_number = Column(String(100), nullable=True)  # 证件号码
    is_active = Column(Boolean, default=True)  # 是否激活
    is_deleted = Column(Boolean, default=False)  # 是否删除

    # 用户可以拥有多个角色
    roles = relationship('Role', secondary=user_role, back_populates='users', lazy='dynamic')

    # 用户可以拥有多个部门
    departments = relationship('Department', secondary=user_department, back_populates='users', lazy='dynamic')

    # 关联访客
    visitors = relationship("Visitor", back_populates="user", lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'gender': self.gender,
            'id_type': self.id_type,
            'id_number': self.id_number,
            'phone_number': self.phone_number,
            'is_active': self.is_active,
        }

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


