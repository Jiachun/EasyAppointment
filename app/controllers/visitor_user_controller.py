# -*- coding: utf-8 -*-
"""
# 文件名称: controllers/visitor_user_controller.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-11
# 版本: 1.0
# 描述: 普通用户的访客信息管理的逻辑控制器
"""

from datetime import datetime

from app.models import Visitor
from extensions.db import db
from utils.format_utils import format_response
from utils.validate_utils import validate_name, validate_gender, validate_id_type, validate_id_number, \
    validate_phone_number


class VisitorUserController:
    @staticmethod
    def get_all_visitors(user):
        """获取当前用户的所有访客信息"""

        # 查找现有的访客信息
        visitors = Visitor.query.filter_by(user_id=user.id, is_deleted=False).all()

        # 返回脱敏后的访客信息
        return format_response(True, {"visitors": [visitor.to_mask() for visitor in visitors]}), 200

    @staticmethod
    def get_visitor_by_id(user, visitor_id):
        """根据访客ID获取访客信息"""

        # 查找现有的访客信息
        visitor = Visitor.query.filter_by(user_id=user.id, id=visitor_id, is_deleted=False).first()

        if visitor:
            # 返回脱敏后的访客信息
            return format_response(True, visitor.to_mask()), 200

        return format_response(False, error='访客未找到'), 404

    @staticmethod
    def create_visitor(user, data):
        """为当前用户添加访客信息"""

        # 校验姓名格式是否正确
        if 'name' not in data or not data['name']:
            return format_response(False, error='姓名不能为空'), 400
        if not validate_name(data['name'].strip()):
            return format_response(False, error='姓名格式有误'), 400

        # 校验性别是否正确
        if 'gender' not in data or not data['gender']:
            return format_response(False, error='性别不能为空'), 400
        if not validate_gender(data['gender'].strip()):
            return format_response(False, error='性别格式有误'), 400

        # 校验证件类型是否正确
        if 'id_type' not in data or not data['id_type']:
            return format_response(False, error='证件类型不能为空'), 400
        if not validate_id_type(data['id_type'].strip()):
            return format_response(False, error='证件类型有误'), 400

        # 校验证件号码是否存在并有效
        if 'id_number' not in data or not data['id_number']:
            return format_response(False, error='证件号码不能为空'), 400
        if not validate_id_number(data['id_type'].strip(), data['id_number'].strip()):
            return format_response(False, error='证件号码不合法'), 400
        if Visitor.query.filter_by(id_number=data['id_number'].strip(), is_deleted=False, user_id=user.id).first():
            return format_response(False, error='证件号码已存在'), 400

        # 校验手机号码是否存在并有效
        if 'phone_number' not in data or not data['phone_number']:
            return format_response(False, error='手机号码不能为空'), 400
        if not validate_phone_number(data['phone_number'].strip()):
            return format_response(False, error='手机号码格式有误'), 400
        if Visitor.query.filter_by(phone_number=data['phone_number'].strip(), is_deleted=False,
                                   user_id=user.id).first():
            return format_response(False, error='手机号码已存在'), 400

        visitor = Visitor(
            name=data['name'].strip(),
            gender=data['gender'].strip(),
            id_type=data['id_type'].strip(),
            id_number=data['id_number'].strip(),
            phone_number=data['phone_number'].strip(),
            user_id=user.id,
            is_deleted=False,
        )

        # 提交数据库更新
        try:
            db.session.add(visitor)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return format_response(False, error=f'数据库更新失败: {str(e)}'), 500

        # 返回脱敏后的访客信息
        return format_response(True, visitor.to_mask()), 200

    @staticmethod
    def delete_visitor(user, visitor_id):
        """根据访客ID删除访客信息"""

        # 查找现有的访客信息
        visitor = Visitor.query.filter_by(id=visitor_id, user_id=user.id, is_deleted=False).first()

        if visitor:
            visitor.is_deleted = True
            visitor.deleted_at = datetime.now()

            # 提交数据库更新
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return format_response(False, error=f'数据库更新失败: {str(e)}'), 500
            return format_response(True, {'message': '访客删除成功'}), 200

        return format_response(False, error='访客未找到'), 404
