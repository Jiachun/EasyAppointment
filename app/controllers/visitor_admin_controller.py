# -*- coding: utf-8 -*-
"""
# 文件名称: controllers/visitor_admin_controller.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-04
# 版本: 1.0
# 描述: 管理员的访客信息管理的逻辑控制器。
"""

import json
from datetime import datetime

from sqlalchemy import asc, desc

from app.models import User, Visitor
from extensions.db import db
from utils.format_utils import format_response
from utils.validate_utils import validate_phone_number, validate_name, validate_gender, validate_id_type, \
    validate_id_number


class VisitorAdminController:
    @staticmethod
    def get_visitors_by_user(user_id):
        """根据用户ID获取指定用户的所有访客信息"""

        # 查找现有的用户信息
        user = User.query.filter_by(id=user_id, is_deleted=False).first()

        if not user:
            return format_response(False, error='用户未找到'), 404

        return format_response(True, {"visitors": [visitor.to_dict() for visitor in user.visitors]}), 200

    @staticmethod
    def get_all_visitors(page=1, per_page=10):
        """获取所有访客信息"""

        # 分页
        paginated_visitors = Visitor.query.filter_by(is_deleted=False).paginate(page=page, per_page=per_page,
                                                                                error_out=False)

        # 返回分页后的数据、总页数、当前页和每页记录数
        return format_response(True, {
            "visitors": [visitor.to_dict() for visitor in paginated_visitors.items],
            "total_pages": paginated_visitors.pages,
            "current_page": page,
            "per_page": per_page
        }), 200

    @staticmethod
    def get_visitor_by_id(visitor_id):
        """根据访客ID获取访客信息"""
        visitor = Visitor.query.filter_by(id=visitor_id, is_deleted=False).first()
        if visitor:
            return format_response(True, visitor.to_dict()), 200
        return format_response(False, error='访客未找到'), 404

    @staticmethod
    def create_visitor(data):
        """创建访客信息"""

        # 查找现有的用户的访客列表
        if 'user_id' not in data or not data['user_id']:
            return format_response(False, error='用户不能为空'), 400

        user = User.query.filter_by(id=data['user_id'], is_deleted=False).first()

        if not user:
            return format_response(False, error='用户未找到'), 404

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
        if Visitor.query.filter_by(id_number=data['id_number'].strip(), is_deleted=False,
                                   user_id=data['user_id']).first():
            return format_response(False, error='证件号码已存在'), 400

        # 校验手机号码是否存在并有效
        if 'phone_number' not in data or not data['phone_number']:
            return format_response(False, error='手机号码不能为空'), 400
        if not validate_phone_number(data['phone_number'].strip()):
            return format_response(False, error='手机号码格式有误'), 400
        if Visitor.query.filter_by(phone_number=data['phone_number'].strip(), is_deleted=False,
                                   user_id=data['user_id']).first():
            return format_response(False, error='手机号码已存在'), 400

        visitor = Visitor(
            name=data['name'].strip(),
            gender=data['gender'].strip(),
            id_type=data['id_type'].strip(),
            id_number=data['id_number'].strip(),
            phone_number=data['phone_number'].strip(),
            user_id=data['user_id'],
            is_deleted=False,
        )

        # 提交数据库更新
        try:
            db.session.add(visitor)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return format_response(False, error=f'数据库更新失败: {str(e)}'), 500

        return format_response(True, visitor.to_dict()), 200

    @staticmethod
    def update_visitor(visitor_id, data):
        """更新访客信息"""

        # 查找现有的访客信息
        visitor = Visitor.query.filter_by(id=visitor_id, is_deleted=False).first()
        if not visitor:
            return format_response(False, error='访客未找到'), 404

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
        if Visitor.query.filter(Visitor.id_number == data['id_number'].strip(), Visitor.id != visitor_id,
                                Visitor.is_deleted == False, Visitor.user_id == data['user_id']).first():
            return format_response(False, error='证件号码已存在'), 400

        # 校验手机号码是否存在并有效
        if 'phone_number' not in data or not data['phone_number']:
            return format_response(False, error='手机号码不能为空'), 400
        if not validate_phone_number(data['phone_number'].strip()):
            return format_response(False, error='手机号码格式有误'), 400
        if Visitor.query.filter(Visitor.phone_number == data['phone_number'].strip(), Visitor.id != visitor_id,
                                Visitor.is_deleted == False, Visitor.user_id == data['user_id']).first():
            return format_response(False, error='手机号码已存在'), 400

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

        visitor.name = data['name'].strip()
        visitor.gender = data['gender'].strip()
        visitor.id_type = data['id_type'].strip()
        visitor.id_number = data['id_number'].strip()
        visitor.phone_number = data['phone_number'].strip()

        # 提交数据库更新
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return format_response(False, error=f'数据库更新失败: {str(e)}'), 500

        return format_response(True, visitor.to_dict()), 200

    @staticmethod
    def delete_visitor(visitor_id):
        """删除访客信息"""

        # 查找现有的访客信息
        visitor = Visitor.query.filter_by(id=visitor_id, is_deleted=False).first()

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

    @staticmethod
    def search_visitors(json_string, page=1, per_page=10, sort_field='id', sort_order='asc'):
        """检索访客信息"""

        # 将参数中的json字符串转换成字典
        filters = {}
        if json_string:
            try:
                filters = json.loads(json_string)  # 将字符串转换为字典
            except ValueError:
                return format_response(False, error='无效的 JSON'), 400

        # 检查 sort_field 是否是 Visitor 模型中的有效列
        if sort_field not in Visitor.__table__.columns:
            return format_response(False, error='无效的排序字段'), 400

        # 创建查询对象
        query = Visitor.query.filter(Visitor.is_deleted == False)

        # 如果有姓名的条件
        if filters.get('name'):
            query = query.filter(Visitor.name.contains(filters['name']))

        # 如果有手机号码的条件
        if filters.get('phone_number'):
            query = query.filter(Visitor.phone_number.contains(filters['phone_number']))

        # 如果有性别的条件
        if filters.get('gender'):
            query = query.filter(Visitor.gender == filters['gender'])

        # 如果有证件类型的条件
        if filters.get('id_type'):
            query = query.filter(Visitor.id_type == filters['id_type'])

        # 如果有证件号码的条件
        if filters.get('id_number'):
            query = query.filter(Visitor.id_number.contains(filters['id_number']))

        # 动态排序，确保sort_field是数据库表中的有效字段
        if sort_order.lower() == 'asc':
            query = query.order_by(asc(getattr(Visitor, sort_field)))
        elif sort_order.lower() == 'desc':
            query = query.order_by(desc(getattr(Visitor, sort_field)))
        else:
            # 如果排序顺序无效，则默认使用升序
            query = query.order_by(asc(getattr(Visitor, sort_field)))

        # 分页
        paginated_visitors = query.paginate(page=page, per_page=per_page, error_out=False)

        # 返回分页后的数据、总页数、当前页和每页记录数
        return format_response(True, {
            "visitors": [visitor.to_dict() for visitor in paginated_visitors.items],
            "total_pages": paginated_visitors.pages,
            "current_page": page,
            "per_page": per_page
        }), 200
