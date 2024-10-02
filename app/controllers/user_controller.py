# -*- coding: utf-8 -*-
"""
# 文件名称: controllers/user_controller.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-01
# 版本: 1.0
# 描述: 用户业务逻辑控制器。
"""

from app.models import User
from extensions.db import db
from utils.validate_utils import validate_phone_number


class UserController:
    @staticmethod
    def get_all_users(page=1, per_page=10):
        """获取所有用户信息"""

        # 分页
        paginated_users = User.query.paginate(page=page, per_page=per_page, error_out=False)

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
        user = User.query.get(user_id)
        if user:
            return user.to_dict(), 200
        return {'error': '用户未找到'}, 404


    @staticmethod
    def create_user(data):
        """创建用户信息"""

        # 校验手机号码是否存在并有效
        if 'phone_number' not in data:
            return {'error': '手机号码不能为空'}, 400
        if not validate_phone_number(data['phone_number']):
            return {'error': '手机号码格式有误'}, 400
        if User.query.filter_by(phone_number=data['phone_number']).first():
            return {'error': '手机号码已存在'}, 400

        # 校验用户名是否存在并有效
        if 'username' not in data or len(data['name']) < 3:
            return {'error': '用户名不能为空且至少为3个字符'}, 400
        if User.query.filter_by(username=data['username']).first():
            return {'error': '用户名已存在'}, 400

        # 校验密码是否存在并有效


        # 校验姓名格式是否正确

        user = User(
            username=data['username'],
            password_hash=data['password_hash'],
            phone_number=data['phone_number'],
            openid = data.get('openid', ''),
            name = data.get('name', ''),
            gender = data.get('gender', ''),
            id_type = data.get('id_type', ''),
            id_number = data.get('id_number', ''),
            is_staff = data.get('is_staff', False),
            is_active = True,
            is_deleted = False,
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

        # 校验手机号是否有效

        # 查找现有的用户信息
        user = User.query.filter_by(id=user_id, is_deleted=False).first()
        if not user:
            return {'error': '用户未找到'}, 404

        # 更新用户信息
        if 'username' in data:
            user.username = data['username']
        if 'password_hash' in data:
            user.password_hash = data['password_hash']
        if 'phone_number' in data:
            user.phone_number = data['phone_number']
        if 'openid' in data:
            user.openid = data['openid']
        if 'name' in data:
            user.name = data['name']
        if 'gender' in data:
            user.gender = data['gender']
        if 'id_type' in data:
            user.id_type = data['id_type']
        if 'id_number' in data:
            user.id_number = data['id_number']
        if 'is_staff' in data:
            user.is_staff = data['is_staff']
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


    @staticmethod
    def search_users(name=None, phone=None, id_number=None, gender=None, page=1, per_page=10):
        """根据姓名、手机号、身份证号和性别进行多条件分页查询"""
        query = User.query

        if name:
            query = query.filter((User.first_name.like(f"%{name}%")) | (User.last_name.like(f"%{name}%")))
        if phone:
            query = query.filter(User.phone_number.like(f"%{phone}%"))
        if id_number:
            query = query.filter(User.id_number.like(f"%{id_number}%"))
        if gender:
            query = query.filter(User.gender == gender)

        # 分页
        paginated_users = query.paginate(page=page, per_page=per_page, error_out=False)

        return paginated_users.items, paginated_users.pages  # 返回分页后的数据和总页数