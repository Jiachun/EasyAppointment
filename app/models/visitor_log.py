# -*- coding: utf-8 -*-
"""
# 文件名称: models/visitor_log.py
# 作者: 罗嘉淳
# 创建日期: 2024-09-30
# 版本: 1.0
# 描述: 访客记录模型文件。
"""

from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime

from extensions.db import db
from utils.crypto_utils import aes256_encrypt_sensitive, aes256_decrypt_sensitive
from utils.mask_utils import mask_name, mask_id_number, mask_phone_number, mask_org_name
from .visitor import Visitor


# 访客记录模型
class VisitorLog(db.Model):
    __tablename__ = 'visitor_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)  # 访客记录ID
    visit_time = Column(DateTime, nullable=False, index=True)  # 来访时间
    leave_time = Column(DateTime, nullable=False)  # 离校时间
    campus = Column(String(50), nullable=False)  # 校区
    visit_type = Column(String(50), nullable=False)  # 来访类型
    _visitor_name = Column('visitor_name', String(255), nullable=False, index=True)  # 访客姓名
    _visitor_phone_number = Column('visitor_phone_number', String(255), nullable=False, index=True)  # 访客手机号码
    visitor_gender = Column(String(10), nullable=False)  # 访客性别
    visitor_id_type = Column(String(50), nullable=False)  # 访客证件类型
    _visitor_id_number = Column('visitor_id_number', String(255), nullable=False)  # 访客证件号码
    _visitor_org = Column('visitor_org', String(255), nullable=True)  # 访客所属单位
    accompanying_people = Column(String(100), nullable=True)  # 随行人员ID（逗号分隔）
    _visited_person_name = Column('visited_person_name', String(255), nullable=True)  # 被访人姓名
    _visited_person_org = Column('visited_person_org', String(255), nullable=True, index=True)  # 被访人部门
    reason = Column(String(255), nullable=True)  # 访问原因
    license_plate = Column(String(20), nullable=True)  # 车牌号码
    is_approved = Column(Boolean, nullable=True)  # 是否审批通过
    approval_note = Column(String(255), nullable=True)  # 审批备注字段
    approved_at = Column(DateTime, nullable=True)  # 审批时间
    _approver = Column('approver', String(255), nullable=True)  # 审批人
    entry_time = Column(DateTime, nullable=True)  # 进校时间
    _verifier = Column('verifier', String(255), nullable=True)  # 核验人
    is_cancelled = Column(Boolean, nullable=True)  # 是否取消
    cancelled_at = Column(DateTime, nullable=True)  # 取消时间
    is_active = Column(Boolean, default=True, nullable=False, index=True)  # 是否激活，当关联用户注销后设置为冻结状态
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)  # 逻辑删除标记
    created_at = Column(DateTime, default=datetime.now, nullable=False)  # 创建时间，用于记录何时创建
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)  # 更新时间，用于记录何时更新
    deleted_at = Column(DateTime, nullable=True)  # 删除时间，用于记录何时删除

    # visitor_name 属性
    @property
    def visitor_name(self):
        return aes256_decrypt_sensitive(self._visitor_name)

    @visitor_name.setter
    def visitor_name(self, value):
        self._visitor_name = aes256_encrypt_sensitive(value)

    # visitor_id_number 属性
    @property
    def visitor_id_number(self):
        return aes256_decrypt_sensitive(self._visitor_id_number)

    @visitor_id_number.setter
    def visitor_id_number(self, value):
        self._visitor_id_number = aes256_encrypt_sensitive(value)

    # visitor_phone_number 属性
    @property
    def visitor_phone_number(self):
        return aes256_decrypt_sensitive(self._visitor_phone_number)

    @visitor_phone_number.setter
    def visitor_phone_number(self, value):
        self._visitor_phone_number = aes256_encrypt_sensitive(value)

    # visitor_org 属性
    @property
    def visitor_org(self):
        return aes256_decrypt_sensitive(self._visitor_org)

    @visitor_org.setter
    def visitor_org(self, value):
        self._visitor_org = aes256_encrypt_sensitive(value)

    # visited_person_name 属性
    @property
    def visited_person_name(self):
        return aes256_decrypt_sensitive(self._visited_person_name)

    @visited_person_name.setter
    def visited_person_name(self, value):
        self._visited_person_name = aes256_encrypt_sensitive(value)

    # visited_person_org 属性
    @property
    def visited_person_org(self):
        return aes256_decrypt_sensitive(self._visited_person_org)

    @visited_person_org.setter
    def visited_person_org(self, value):
        self._visited_person_org = aes256_encrypt_sensitive(value)

    # approver 属性
    @property
    def approver(self):
        return aes256_decrypt_sensitive(self._approver)

    @approver.setter
    def approver(self, value):
        self._approver = aes256_encrypt_sensitive(value)

    # verifier 属性
    @property
    def verifier(self):
        return aes256_decrypt_sensitive(self._verifier)

    @verifier.setter
    def verifier(self, value):
        self._verifier = aes256_encrypt_sensitive(value)

    def __repr__(self):
        return f'<VisitorLog {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'visit_time': self.visit_time,
            'leave_time': self.leave_time,
            'campus': self.campus,
            'visit_type': self.visit_type,
            'visitor_name': self.visitor_name,
            'visitor_phone_number': self.visitor_phone_number,
            'visitor_gender': self.visitor_gender,
            'visitor_id_type': self.visitor_id_type,
            'visitor_id_number': self.visitor_id_number,
            'visitor_org': self.visitor_org,
            'visited_person_name': self.visited_person_name,
            'visited_person_org': self.visited_person_org,
            'reason': self.reason,
            'license_plate': self.license_plate,
            'is_approved': self.is_approved,
            'approval_note': self.approval_note,
            'approved_at': self.approved_at,
            'approver': self.approver,
            'entry_time': self.entry_time,
            'verifier': self.verifier,
            'is_cancelled': self.is_cancelled,
            'cancelled_at': self.cancelled_at,
            'accompanying_people': self.get_accompanying_people_info(need_mask=False),
        }

    def to_mask(self):
        return {
            'id': self.id,
            'visit_time': self.visit_time,
            'leave_time': self.leave_time,
            'campus': self.campus,
            'visit_type': self.visit_type,
            'visitor_name': mask_name(self.visitor_name),
            'visitor_phone_number': mask_phone_number(self.visitor_phone_number),
            'visitor_gender': self.visitor_gender,
            'visitor_id_type': self.visitor_id_type,
            'visitor_id_number': mask_id_number(self.visitor_id_number),
            'visitor_org': mask_org_name(self.visitor_org),
            'visited_person_name': mask_name(self.visited_person_name),
            'visited_person_org': mask_org_name(self.visited_person_org),
            'reason': self.reason,
            'license_plate': self.license_plate,
            'is_approved': self.is_approved,
            'approval_note': self.approval_note,
            'approved_at': self.approved_at,
            'approver': mask_name(self.approver),
            'entry_time': self.entry_time,
            'verifier': mask_name(self.verifier),
            'is_cancelled': self.is_cancelled,
            'cancelled_at': self.cancelled_at,
            'accompanying_people': self.get_accompanying_people_info(need_mask=True),
        }

    def get_accompanying_people_info(self, need_mask=True):
        """获取访客记录中随行人员的详细信息"""

        # 将 accompanying_people 逗号分隔的字符串转换为 ID 列表
        accompanying_people_ids = self.accompanying_people.split(',')

        # 转换为整数列表（假设 ID 都是数字）
        accompanying_people_ids = [int(visitor_id) for visitor_id in accompanying_people_ids]

        # 根据 ID 列表查询所有对应的访客信息
        accompanying_people = Visitor.query.filter(Visitor.id.in_(accompanying_people_ids)).all()

        accompanying_people_info = []
        # 判断数据是否需要脱敏处理
        if need_mask is True:
            accompanying_people_info = [visitor.to_mask() for visitor in accompanying_people]
        if need_mask is False:
            accompanying_people_info = [visitor.to_dict() for visitor in accompanying_people]

        return accompanying_people_info
