# -*- coding: utf-8 -*-
"""
# 文件名称: controllers/visitor_controller.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-04
# 版本: 1.0
# 描述: 访客信息逻辑控制器。
"""

from app.models import User, Visitor
from extensions.db import db
from utils.validate_utils import validate_phone_number, validate_name, validate_gender, validate_id_type, validate_id_number


class VisitorController:
    @staticmethod
    def get_visitors_by_user(data):
        """获取用户的所有访客信息"""

        if 'user_id' not in data:
            return {'error': '用户不能为空'}, 400

        # 查找现有的用户信息
        user = User.query.filter_by(id=data['user_id'], is_deleted=False).first()

        if not user:
            return {'error': '用户未找到'}, 404

        return {"visitors": [visitor.to_dict() for visitor in user.visitors]}, 200


    @staticmethod
    def get_visitor_by_id(visitor_id):
        """根据访客ID获取访客信息"""
        visitor = Visitor.query.filter_by(id=visitor_id, is_deleted=False).first()
        if visitor:
            return visitor.to_dict(), 200
        return {'error': '访客未找到'}, 404


    @staticmethod
    def create_visitor(data):
        """创建访客信息"""

        # 查找现有的用户的访客列表
        if 'user_id' not in data:
            return {'error': '用户不能为空'}, 400

        user = User.query.filter_by(id=data['user_id'], is_deleted=False).first()

        if not user:
            return {'error': '用户未找到'}, 404

        # 校验姓名格式是否正确
        if 'name' not in data:
            return {'error': '姓名不能为空'}, 400
        if not validate_name(data['name']):
            return {'error': '姓名格式有误'}, 400

        # 校验性别是否正确
        if 'gender' not in data:
            return {'error': '性别不能为空'}, 400
        if not validate_gender(data['gender']):
            return {'error': '性别格式有误'}, 400

        # 校验证件类型是否正确
        if 'id_type' not in data:
            return {'error': '证件类型不能为空'}, 400
        if not validate_id_type(data['id_type']):
            return {'error': '证件类型有误'}, 400

        # 校验证件号码是否存在并有效
        if 'id_number' not in data:
            return {'error': '证件号码不能为空'}, 400
        if not validate_id_number(data['id_type'], data['id_number']):
            return {'error': '证件号码不合法'}, 400
        if Visitor.query.filter_by(id_number=data['id_number'], is_deleted=False, user_id=data['user_id']).first():
            return {'error': '证件号码已存在'}, 400

        # 校验手机号码是否存在并有效
        if 'phone_number' not in data:
            return {'error': '手机号码不能为空'}, 400
        if not validate_phone_number(data['phone_number']):
            return {'error': '手机号码格式有误'}, 400
        if Visitor.query.filter_by(phone_number=data['phone_number'], is_deleted=False, user_id=data['user_id']).first():
            return {'error': '手机号码已存在'}, 400

        visitor = Visitor(
            name=data['name'],
            gender=data['gender'],
            id_type=data['id_type'],
            id_number=data['id_number'],
            phone_number=data['phone_number'],
            is_deleted=False,
        )

        # 提交数据库更新
        try:
            db.session.add(visitor)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': '数据库更新失败: {}'.format(str(e))}, 500

        return visitor.to_dict(), 200


    @staticmethod
    def update_visitor(visitor_id, data):
        """更新访客信息"""

        # 查找现有的访客信息
        visitor = Visitor.query.filter_by(id=visitor_id, is_deleted=False).first()
        if not visitor:
            return {'error': '访客未找到'}, 404

        # 校验证件类型是否正确
        if 'id_type' not in data:
            return {'error': '证件类型不能为空'}, 400
        if not validate_id_type(data['id_type']):
            return {'error': '证件类型有误'}, 400

        # 校验证件号码是否存在并有效
        if 'id_number' not in data:
            return {'error': '证件号码不能为空'}, 400
        if not validate_id_number(data['id_type'], data['id_number']):
            return {'error': '证件号码不合法'}, 400
        if Visitor.query.filter(Visitor.id_number==data['id_number'], Visitor.id != visitor_id, Visitor.is_deleted==False, Visitor.user_id==data['user_id']).first():
            return {'error': '证件号码已存在'}, 400

        # 校验手机号码是否存在并有效
        if 'phone_number' not in data:
            return {'error': '手机号码不能为空'}, 400
        if not validate_phone_number(data['phone_number']):
            return {'error': '手机号码格式有误'}, 400
        if Visitor.query.filter(Visitor.phone_number==data['phone_number'], Visitor.id != visitor_id, Visitor.is_deleted==False, Visitor.user_id==data['user_id']).first():
            return {'error': '手机号码已存在'}, 400

        # 校验姓名格式是否正确
        if 'name' not in data:
            return {'error': '姓名不能为空'}, 400
        if not validate_name(data['name']):
            return {'error': '姓名格式有误'}, 400

        # 校验性别是否正确
        if 'gender' not in data:
            return {'error': '性别不能为空'}, 400
        if not validate_gender(data['gender']):
            return {'error': '性别格式有误'}, 400

        visitor.name = data['name']
        visitor.gender = data['gender']
        visitor.id_type = data['id_type']
        visitor.id_number = data['id_number']
        visitor.phone_number = data['phone_number']

        # 提交数据库更新
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': '数据库更新失败: {}'.format(str(e))}, 500

        return visitor.to_dict(), 200


    @staticmethod
    def delete_visitor(visitor_id):
        """删除访客信息"""

        # 查找现有的访客信息
        visitor = Visitor.query.filter_by(id=visitor_id, is_deleted=False).first()

        if visitor:
            visitor.is_deleted = True

            # 提交数据库更新
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return {'error': '数据库更新失败: {}'.format(str(e))}, 500
            return {'message': '访客删除成功'}, 200

        return {'error': '访客未找到'}, 404