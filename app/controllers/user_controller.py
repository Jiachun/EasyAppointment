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
        if 'username' not in data or not data['username']:
            return {'error': '用户名不能为空'}, 400
        if not validate_username(data['username']):
            return {'error': '用户名格式有误'}, 400
        if User.query.filter_by(username=data['username'], is_deleted=False).first():
            return {'error': '用户名已存在'}, 400

        # 校验密码是否有效
        if 'password_hash' not in data or not data['password_hash']:
            return {'error': '密码不能为空'}, 400

        # 校验手机号码是否存在并有效
        if 'phone_number' not in data or not data['phone_number']:
            return {'error': '手机号码不能为空'}, 400
        if not validate_phone_number(data['phone_number']):
            return {'error': '手机号码格式有误'}, 400
        if User.query.filter_by(phone_number=data['phone_number'], is_deleted=False).first():
            return {'error': '手机号码已存在'}, 400

        # 校验姓名格式是否正确
        if 'name' not in data or not data['name']:
            return {'error': '姓名不能为空'}, 400
        if not validate_name(data['name']):
            return {'error': '姓名格式有误'}, 400

        # 校验性别是否正确
        if 'gender' not in data or not data['gender']:
            return {'error': '性别不能为空'}, 400
        if validate_gender(data['gender']):
            return {'error': '性别格式有误'}, 400

        # 校验证件类型是否正确
        if 'id_type' not in data or not data['id_type']:
            return {'error': '证件类型不能为空'}, 400
        if not validate_id_type(data['id_type']):
            return {'error': '证件类型有误'}, 400

        # 校验证件号码是否合法
        if 'id_number' not in data or not data['id_number']:
            return {'error': '证件号码不能为空'}, 400
        if not validate_id_number(data['id_type'], data['id_number']):
            return {'error': '证件号码不合法'}, 400

        user = User(
            username=data['username'],
            password_hash=generate_password_hash(data['password_hash'],method='scrypt'),
            phone_number=data['phone_number'],
            name=data['name'],
            gender=data['gender'],
            id_type=data['id_type'],
            id_number=data['id_number'],
            openid=None,
            is_active=True,
            is_deleted=False,
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

        # 校验用户名是否存在并有效
        if 'username' not in data or not data['username']:
            return {'error': '用户名不能为空'}, 400
        if not validate_username(data['username']):
            return {'error': '用户名格式有误'}, 400
        if User.query.filter(User.username==data['username'], User.id!=user_id, User.is_deleted==False).first():
            return {'error': '用户名已存在'}, 400

        # 校验手机号码是否存在并有效
        if 'phone_number' not in data or not data['phone_number']:
            return {'error': '手机号码不能为空'}, 400
        if not validate_phone_number(data['phone_number']):
            return {'error': '手机号码格式有误'}, 400
        if User.query.filter(User.phone_number==data['phone_number'], User.id!=user_id, User.is_deleted==False).first():
            return {'error': '手机号码已存在'}, 400

        # 校验姓名格式是否正确
        if 'name' not in data or not data['name']:
            return {'error': '姓名不能为空'}, 400
        if not validate_name(data['name']):
            return {'error': '姓名格式有误'}, 400

        # 校验性别格式是否正确
        if 'gender' not in data or not data['gender']:
            return {'error': '性别不能为空'}, 400
        if not validate_gender(data['gender']):
            return {'error': '性别格式有误'}, 400

        # 校验证件类型是否正确
        if 'id_type' not in data or not data['id_type']:
            return {'error': '证件类型不能为空'}, 400
        if not validate_id_type(data['id_type']):
            return {'error': '证件类型有误'}, 400

        # 校验证件号码是否合法
        if 'id_number' not in data or not data['id_number']:
            return {'error': '证件号码不能为空'}, 400
        if not validate_id_number(data['id_type'], data['id_number']):
            return {'error': '证件号码不合法'}, 400

        user.username = data['username']
        user.phone_number = data['phone_number']
        user.name = data['name']
        user.gender = data['gender']
        user.id_type = data['id_type']
        user.id_number = data['id_number']

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
    def search_users(filters, page=1, per_page=10):
        """检索用户信息"""

        # 创建查询对象
        query = User.query

        # 如果有用户名的条件
        if filters.get('username'):
            query = query.filter(User.username.contains(filters['username']))

        # 如果有姓名的条件
        if filters.get('name'):
            query = query.filter(User.name.contains(filters['name']))

        # 如果有手机号码的条件
        if filters.get('phone_number'):
            query = query.filter(User.phone_number.contains(filters['phone_number']))

        # 如果有性别的条件
        if filters.get('gender'):
            query = query.filter(User.gender == filters['gender'])

        # 如果有证件类型的条件
        if filters.get('id_type'):
            query = query.filter(User.id_type == filters['id_type'])

        # 如果有证件号码的条件
        if filters.get('id_number'):
            query = query.filter(User.id_number.contains(filters['id_number']))

        # 如果有激活状态的条件
        if filters.get('is_active'):
            query = query.filter(User.is_active==filters['is_active'])

        # 分页
        paginated_users = query.filter(User.is_deleted==False).paginate(page=page, per_page=per_page, error_out=False)

        # 返回分页后的数据、总页数、当前页和每页记录数
        return {
            "users": [user.to_dict() for user in paginated_users.items],
            "total_pages": paginated_users.pages,
            "current_page": page,
            "per_page": per_page
        }, 200