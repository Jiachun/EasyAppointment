# -*- coding: utf-8 -*-
"""
# 文件名称: controllers/user_controller.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-01
# 版本: 1.0
# 描述: 用户信息逻辑控制器。
"""

from werkzeug.security import generate_password_hash
from app.models import User
from extensions.db import db
from utils.validate_utils import validate_username, validate_phone_number, validate_name, validate_gender, validate_id_type, validate_id_number


class UserController:
    @staticmethod
    def get_all_users(page=1, per_page=10):
        """获取所有用户信息"""

        # 分页
        paginated_users = User.query.filter_by(is_deleted=False).paginate(page=page, per_page=per_page, error_out=False)

        # 返回分页后的数据、总页数、当前页和每页记录数
        return {
            "users": [user.to_dict() for user in paginated_users.items],
            "total_pages": paginated_users.pages,
            "current_page": page,
            "per_page": per_page
        }, 200


    @staticmethod
    def get_user_by_id(user_id):
        """根据ID获取用户信息"""
        user = User.query.filter_by(id=user_id, is_deleted=False).first()
        if user:
            return user.to_dict(), 200
        return {'error': '用户未找到'}, 404


    @staticmethod
    def create_user(data):
        """创建用户信息"""

        # 校验用户名是否存在并有效
        if 'username' not in data:
            return {'error': '用户名不能为空'}, 400
        if not validate_username(data['username']):
            return {'error': '用户名格式有误'}, 400
        if User.query.filter_by(username=data['username'], is_deleted=False).first():
            return {'error': '用户名已存在'}, 400

        # 校验密码是否有效
        if 'password' not in data:
            return {'error': '密码不能为空'}, 400

        # 校验手机号码是否存在并有效
        if 'phone_number' not in data:
            return {'error': '手机号码不能为空'}, 400
        if not validate_phone_number(data['phone_number']):
            return {'error': '手机号码格式有误'}, 400
        if User.query.filter_by(phone_number=data['phone_number'], is_deleted=False).first():
            return {'error': '手机号码已存在'}, 400

        # 校验姓名格式是否正确
        if 'name' in data and not validate_name(data['name']):
            return {'error': '姓名格式有误'}, 400

        # 校验性别是否正确
        if 'gender' in data and not validate_gender(data['gender']):
            return {'error': '性别格式有误'}, 400

        # 校验证件类型是否正确
        if 'id_type' in data and not validate_id_type(data['id_type']):
            return {'error': '证件类型有误'}, 400

        # 校验证件号码是否合法
        if 'id_type' in data and 'id_number' in data and not validate_id_number(data['id_type'], data['id_number']):
            return {'error': '证件号码不合法'}, 400

        user = User(
            username=data['username'],
            password_hash=generate_password_hash(data['password_hash'],method='scrypt'),
            phone_number=data['phone_number'],
            openid = data.get('openid', ''),
            name = data.get('name', ''),
            gender = data.get('gender', ''),
            id_type = data.get('id_type', ''),
            id_number = data.get('id_number', ''),
            is_staff = data.get('is_staff', True),
            is_active = data.get('is_active', True),
            is_deleted = data.get('is_deleted', False),
        )

        # 提交数据库更新
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': '数据库更新失败: {}'.format(str(e))}, 500

        return user.to_dict(), 200


    @staticmethod
    def update_user(user_id, data):
        """更新用户信息"""

        # 查找现有的用户信息
        user = User.query.filter_by(id=user_id, is_deleted=False).first()
        if not user:
            return {'error': '用户未找到'}, 404

        # 校验并更新用户名
        if 'username' in data:
            if not validate_username(data['username']):
                return {'error': '用户名格式有误'}, 400
            if User.query.filter(User.username==data['username'], User.id!=user_id, User.is_deleted==False).first():
                return {'error': '用户名已存在'}, 400
            user.username = data['username']

        # 校验并更新手机号码
        if 'phone_number' in data:
            if not validate_phone_number(data['phone_number']):
                return {'error': '手机号码格式有误'}, 400
            if User.query.filter(User.phone_number==data['phone_number'], User.id!=user_id, User.is_deleted==False).first():
                return {'error': '手机号码已存在'}, 400
            user.phone_number = data['phone_number']

        # 校验并更新姓名
        if 'name' in data:
            if not validate_name(data['name']):
                return {'error': '姓名格式有误'}, 400
            user.name = data['name']

        # 校验并更新性别
        if 'gender' in data:
            if not validate_gender(data['gender']):
                return {'error': '性别格式有误'}, 400
            user.gender = data['gender']

        # 校验并更新证件类型
        if 'id_type' in data:
            if not validate_id_type(data['id_type']):
                return {'error': '证件类型有误'}, 400
            user.id_type = data['id_type']

        # 校验并更新证件号码
        if 'id_type' in data and 'id_number' in data:
            if not validate_id_number(data['id_number'], data['id_number']):
                return {'error': '证件号码不合法'}, 400
            user.id_number = data['id_number']

        # 更新用户类型
        if 'is_staff' in data:
            user.is_staff = data['is_staff']

        # 更新激活状态
        if 'is_active' in data:
            user.is_active = data['is_active']

        # 提交数据库更新
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': '数据库更新失败: {}'.format(str(e))}, 500

        return user.to_dict(), 200


    @staticmethod
    def delete_user(user_id):
        """删除用户信息"""

        # 查找现有的用户信息
        user = User.query.filter_by(id=user_id, is_deleted=False).first()

        if user:
            user.is_deleted = True

            # 提交数据库更新
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return {'error': '数据库更新失败: {}'.format(str(e))}, 500
            return {'message': '用户删除成功'}, 200

        return {'error': '用户未找到'}, 404