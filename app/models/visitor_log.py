# -*- coding: utf-8 -*-
"""
# 文件名称: models/visitor_log.py
# 作者: 罗嘉淳
# 创建日期: 2024-09-30
# 版本: 1.0
# 描述: 访客记录模型文件。
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from extensions.db import db


# 访客记录模型
class VisitorLog(db.Model):
    __tablename__ = 'visitor_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)  # 访客记录ID
    visit_time = Column(DateTime, nullable=False)  # 来访时间
    entry_time = Column(DateTime, nullable=True)  # 进校时间
    leave_time = Column(DateTime, nullable=False)  # 离校时间
    campus = Column(String(100), nullable=False)  # 校区
    visit_type = Column(String(50), nullable=False)  # 来访类型
    visitor_org = Column(String(100), nullable=True)  # 访客所属单位
    accompanying_people = Column(db.String(255), nullable=True)  # 随行人员ID（逗号分隔）
    visited_person_name = Column(String(100), nullable=True)  # 被访人姓名
    visited_person_org = Column(String(100), nullable=True)  # 被访人单位
    reason = Column(String(255), nullable=True)  # 访问原因
    license_plate = Column(String(20), nullable=True)  # 车牌号码
    approver = Column(String(100), nullable=True)  # 审批人
    approval_time = Column(DateTime, nullable=True)  # 审批时间
    is_approved = Column(Boolean, nullable=True)  # 是否审批通过
    is_deleted = Column(Boolean, default=False)  # 是否删除
    created_at = Column(DateTime, default=datetime.now())  # 记录创建时间
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())  # 记录更新时间

    def __repr__(self):
        return f'<VisitorLog {self.id}>'