# -*- coding: utf-8 -*-
"""
# 文件名称: models/visitor.py
# 作者: 罗嘉淳
# 创建日期: 2024-09-30
# 版本: 1.0
# 描述: 访客模型文件。
"""
from xmlrpc.client import Boolean

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from extensions.db import db


# 访客模型
class Visitor(db.Model):
    __tablename__ = 'visitors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 访客ID
    name = Column(String(50), nullable=False)  # 姓名
    id_type = Column(String(50), nullable=False)  # 证件类型
    id_number = Column(String(100), nullable=False)  # 证件号码
    phone_number = Column(String(20), nullable=False)  # 手机号码
    is_deleted = Column(Boolean, default=False)  # 是否删除
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)  # 上一级用户ID

    def __repr__(self):
        return f'<Visitor {self.name}>'