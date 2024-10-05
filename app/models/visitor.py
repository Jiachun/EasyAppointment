# -*- coding: utf-8 -*-
"""
# 文件名称: models/visitor.py
# 作者: 罗嘉淳
# 创建日期: 2024-09-30
# 版本: 1.0
# 描述: 访客模型文件。
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from extensions.db import db


# 访客模型
class Visitor(db.Model):
    __tablename__ = 'visitors'

    id = Column(Integer, primary_key=True, autoincrement=True)  # 访客ID
    name = Column(String(50), nullable=False)  # 姓名
    gender = Column(String(10), nullable=False)  # 性别
    id_type = Column(String(50), nullable=False)  # 证件类型
    id_number = Column(String(100), nullable=False)  # 证件号码
    phone_number = Column(String(20), nullable=False)  # 手机号码
    is_deleted = Column(Boolean, default=False)  # 是否删除
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # 上一级用户ID

    # 关联到用户
    user = db.relationship("User", back_populates="visitors", lazy='dynamic')

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