# -*- coding: utf-8 -*-
"""
# 文件名称: models/campus.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-01
# 版本: 1.0
# 描述: 校区模型文件。
"""


from sqlalchemy import Column, Integer, String, Boolean, DateTime
from extensions.db import db
from datetime import datetime


# 访客记录模型
class Campus(db.Model):
    __tablename__ = 'campuses'

    id = Column(Integer, primary_key=True, autoincrement=True)  # 校区ID
    name = Column(String(50), nullable=False)  # 校区名称，唯一
    description = Column(String(255), nullable=True)  # 校区描述（可选）
    is_deleted = Column(Boolean, default=False, nullable=False)  # 逻辑删除标记
    created_at = Column(DateTime, default=datetime.now(), nullable=False)  # 创建时间，用于记录何时创建
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)  # 更新时间，用于记录何时更新
    deleted_at = Column(DateTime, nullable=True)  # 删除时间，用于记录何时删除

    def __repr__(self):
        return f'<Campus {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }