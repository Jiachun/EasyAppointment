# -*- coding: utf-8 -*-
"""
# 文件名称: models/user.py
# 作者: 罗嘉淳
# 创建日期: 2024-09-29
# 版本: 1.0
# 描述: 用户的模型文件。
"""

from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship

from extensions.db import db
from utils.crypto_utils import aes256_encrypt_sensitive, aes256_decrypt_sensitive
from utils.mask_utils import mask_name, mask_id_number, mask_phone_number


# 用户模型
class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)  # 用户ID
    _username = Column('username', String(255), nullable=False, index=True)  # 用户名
    password_hash = Column(String(128), nullable=False)  # 密码
    _phone_number = Column('phone_number', String(255), nullable=False, index=True)  # 手机号码
    openid = Column(String(128), nullable=True)  # OpenID
    _name = Column('name', String(255), nullable=True, index=True)  # 姓名
    gender = Column(String(10), nullable=True)  # 性别
    id_type = Column(String(50), nullable=True)  # 证件类型
    _id_number = Column('id_number', String(255), nullable=True)  # 证件号码
    is_active = Column(Boolean, default=True)  # 激活标记
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)  # 逻辑删除标记
    created_at = Column(DateTime, default=datetime.now, nullable=False)  # 创建时间，用于记录何时创建
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)  # 更新时间，用于记录何时更新
    deleted_at = Column(DateTime, nullable=True)  # 删除时间，用于记录何时删除

    # 定义反向关系
    user_roles = relationship('UserRole', back_populates='user', lazy='dynamic')
    user_departments = relationship('UserDepartment', back_populates='user', lazy='dynamic')
    visitors = relationship("Visitor", back_populates="user", lazy='dynamic')

    # username 属性
    @property
    def username(self):
        return aes256_decrypt_sensitive(self._username)

    @username.setter
    def username(self, value):
        self._username = aes256_encrypt_sensitive(value)

    # phone_number 属性
    @property
    def phone_number(self):
        return aes256_decrypt_sensitive(self._phone_number)

    @phone_number.setter
    def phone_number(self, value):
        self._phone_number = aes256_encrypt_sensitive(value)

    # name 属性
    @property
    def name(self):
        return aes256_decrypt_sensitive(self._name)

    @name.setter
    def name(self, value):
        self._name = aes256_encrypt_sensitive(value)

    # id_number 属性
    @property
    def id_number(self):
        return aes256_decrypt_sensitive(self._id_number)

    @id_number.setter
    def id_number(self, value):
        self._id_number = aes256_encrypt_sensitive(value)

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
        }

    def to_mask(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': mask_name(self.name),
            'gender': self.gender,
            'id_type': self.id_type,
            'id_number': mask_id_number(self.id_number),
            'phone_number': mask_phone_number(self.phone_number),
        }

    def has_permission(self, permission_name):
        """检查用户是否具有某个权限"""
        # 遍历用户的角色，检查每个角色是否关联有指定的权限
        for user_role in self.user_roles.filter_by(is_deleted=False):
            role = user_role.role
            for role_permission in role.role_permissions.filter_by(is_deleted=False):
                permission = role_permission.permission
                if permission.name == permission_name and not permission.is_deleted:
                    return True
        return False


    def get_departments(self):
        """获取用户所属的所有部门"""
        # 遍历用户的所有有效的部门关联记录，返回部门名称列表
        return [user_department.department.name for user_department in
                self.user_departments.filter_by(is_deleted=False)]
