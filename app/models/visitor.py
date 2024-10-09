# -*- coding: utf-8 -*-
"""
# 文件名称: models/visitor.py
# 作者: 罗嘉淳
# 创建日期: 2024-09-30
# 版本: 1.0
# 描述: 访客模型文件。
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from extensions.db import db
from datetime import datetime
from utils.crypto_utils import aes256_encrypt_sensitive, aes256_decrypt_sensitive


# 访客模型
class Visitor(db.Model):
    __tablename__ = 'visitors'

    id = Column(Integer, primary_key=True, autoincrement=True)  # 访客ID
    _name = Column('name', String(255), nullable=False, index=True)  # 姓名
    gender = Column(String(10), nullable=False)  # 性别
    id_type = Column(String(50), nullable=False)  # 证件类型
    _id_number = Column('id_number', String(255), nullable=False)  # 证件号码
    _phone_number = Column('phone_number', String(255), nullable=False, index=True)  # 手机号码
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)  # 所属用户ID
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)  # 逻辑删除标记
    created_at = Column(DateTime, default=datetime.now, nullable=False)  # 创建时间，用于记录何时创建
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)  # 更新时间，用于记录何时更新
    deleted_at = Column(DateTime, nullable=True)  # 删除时间，用于记录何时删除

    # 定义反向关系
    user = db.relationship("User", back_populates="visitors")

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

    # phone_number 属性
    @property
    def phone_number(self):
        return aes256_decrypt_sensitive(self._phone_number)

    @phone_number.setter
    def phone_number(self, value):
        self._phone_number = aes256_encrypt_sensitive(value)

    def __repr__(self):
        return f'<Visitor {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'id_type': self.id_type,
            'id_number': self.id_number,
            'phone_number': self.phone_number,
            'user_id': self.user_id,
        }