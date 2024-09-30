# -*- coding: utf-8 -*-
"""
# 文件名称: models/visitor_log.py
# 作者: 罗嘉淳
# 创建日期: 2024-09-30
# 版本: 1.0
# 描述: 访客记录模型文件。
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from extensions.db import db


# 访客记录模型
class VisitorLog(db.Model):
    __tablename__ = 'visitor_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)  # 访客记录ID
    visit_time = Column(DateTime, nullable=False, default=datetime.now())  # 来访时间
    leave_time = Column(DateTime, nullable=False, default=datetime.now())  # 离校时间
    reason = Column(String(255), nullable=True)  # 访问原因
    is_deleted = Column(Boolean, default=False)  # 是否删除
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)  # 上一级用户ID

    def __repr__(self):
        return f'<Visitor {self.name}>'