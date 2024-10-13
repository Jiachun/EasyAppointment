# -*- coding: utf-8 -*-
"""
# 文件名称: controllers/user_controller.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-01
# 版本: 1.0
# 描述: 用户信息逻辑控制器。
"""

import json
from datetime import datetime

from sqlalchemy import asc, desc
from werkzeug.security import generate_password_hash

from app.models import User, VisitorLog
from extensions.db import db, redis_client
from utils.format_utils import format_response
from utils.validate_utils import validate_username, validate_phone_number, validate_name, validate_gender, \
    validate_id_type, validate_id_number


class UserController:
    @staticmethod
    def get_all_users(page=1, per_page=10):
        """获取所有用户信息"""

        # 分页
        paginated_users = User.query.filter_by(is_deleted=False).paginate(page=page, per_page=per_page, error_out=False)

        # 返回分页后的数据、总页数、当前页和每页记录数
        return format_response(True, {
            "users": [user.to_dict() for user in paginated_users.items],
            "total_pages": paginated_users.pages,
            "current_page": page,
            "per_page": per_page
        }), 200

    @staticmethod
    def get_user_by_id(user_id):
        """根据用户ID获取用户信息"""
        user = User.query.filter_by(id=user_id, is_deleted=False).first()
        if user:
            return format_response(True, user.to_dict()), 200
        return format_response(False, error='用户未找到'), 404

    @staticmethod
    def create_user(data):
        """创建用户信息"""

        # 校验用户名是否存在并有效
        if 'username' not in data or not data['username'].strip():
            return format_response(False, error='用户名不能为空'), 400
        if not validate_username(data['username'].strip()):
            return format_response(False, error='用户名格式有误'), 400
        if User.query.filter_by(username=data['username'].strip(), is_deleted=False).first():
            return format_response(False, error='用户名已存在'), 400

        # 校验密码是否有效
        if 'password_hash' not in data or not data['password_hash'].strip():
            return format_response(False, error='密码不能为空'), 400

        # 校验手机号码是否存在并有效
        if 'phone_number' not in data or not data['phone_number'].strip():
            return format_response(False, error='手机号码不能为空'), 400
        if not validate_phone_number(data['phone_number'].strip()):
            return format_response(False, error='手机号码格式有误'), 400
        if User.query.filter_by(phone_number=data['phone_number'].strip(), is_deleted=False).first():
            return format_response(False, error='手机号码已存在'), 400

        # 校验姓名格式是否正确
        if 'name' not in data or not data['name'].strip():
            return format_response(False, error='姓名不能为空'), 400
        if not validate_name(data['name'].strip()):
            return format_response(False, error='姓名格式有误'), 400

        # 校验性别是否正确
        if 'gender' not in data or not data['gender'].strip():
            return format_response(False, error='性别不能为空'), 400
        if validate_gender(data['gender'].strip()):
            return format_response(False, error='性别格式有误'), 400

        # 校验证件类型是否正确
        if 'id_type' not in data or not data['id_type'].strip():
            return format_response(False, error='证件类型不能为空'), 400
        if not validate_id_type(data['id_type'].strip()):
            return format_response(False, error='证件类型有误'), 400

        # 校验证件号码是否合法
        if 'id_number' not in data or not data['id_number'].strip():
            return format_response(False, error='证件号码不能为空'), 400
        if not validate_id_number(data['id_type'].strip(), data['id_number'].strip()):
            return format_response(False, error='证件号码不合法'), 400

        user = User(
            username=data['username'].strip(),
            password_hash=generate_password_hash(data['password_hash'].strip(), method='scrypt'),
            phone_number=data['phone_number'].strip(),
            name=data['name'].strip(),
            gender=data['gender'].strip(),
            id_type=data['id_type'].strip(),
            id_number=data['id_number'].strip(),
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
            return format_response(False, error=f'数据库更新失败: {str(e)}'), 500

        return format_response(True, user.to_dict()), 200

    @staticmethod
    def update_user(user_id, data):
        """更新用户信息"""

        # 查找现有的用户信息
        user = User.query.filter_by(id=user_id, is_deleted=False).first()
        if not user:
            return format_response(False, error='用户未找到'), 404

        # 校验用户名是否存在并有效
        if 'username' not in data or not data['username'].strip():
            return format_response(False, error='用户名不能为空'), 400
        if not validate_username(data['username'].strip()):
            return format_response(False, error='用户名格式有误'), 400
        if User.query.filter(User.username == data['username'].strip(), User.id != user_id,
                             User.is_deleted == False).first():
            return format_response(False, error='用户名已存在'), 400

        # 校验手机号码是否存在并有效
        if 'phone_number' not in data or not data['phone_number'].strip():
            return format_response(False, error='手机号码不能为空'), 400
        if not validate_phone_number(data['phone_number'].strip()):
            return format_response(False, error='手机号码格式有误'), 400
        if User.query.filter(User.phone_number == data['phone_number'].strip(), User.id != user_id,
                             User.is_deleted == False).first():
            return format_response(False, error='手机号码已存在'), 400

        # 校验姓名格式是否正确
        if 'name' not in data or not data['name'].strip():
            return format_response(False, error='姓名不能为空'), 400
        if not validate_name(data['name'].strip()):
            return format_response(False, error='姓名格式有误'), 400

        # 校验性别格式是否正确
        if 'gender' not in data or not data['gender'].strip():
            return format_response(False, error='性别不能为空'), 400
        if not validate_gender(data['gender'].strip()):
            return format_response(False, error='性别格式有误'), 400

        # 校验证件类型是否正确
        if 'id_type' not in data or not data['id_type'].strip():
            return format_response(False, error='证件类型不能为空'), 400
        if not validate_id_type(data['id_type'].strip()):
            return format_response(False, error='证件类型有误'), 400

        # 校验证件号码是否合法
        if 'id_number' not in data or not data['id_number'].strip():
            return format_response(False, error='证件号码不能为空'), 400
        if not validate_id_number(data['id_type'].strip(), data['id_number'].strip()):
            return format_response(False, error='证件号码不合法'), 400

        user.username = data['username'].strip()
        user.phone_number = data['phone_number'].strip()
        user.name = data['name'].strip()
        user.gender = data['gender'].strip()
        user.id_type = data['id_type'].strip()
        user.id_number = data['id_number'].strip()

        # 提交数据库更新
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return format_response(False, error=f'数据库更新失败: {str(e)}'), 500

        return format_response(True, user.to_dict()), 200

    @staticmethod
    def delete_user(user_id):
        """删除用户信息"""

        # 查找现有的用户信息
        user = User.query.filter_by(id=user_id, is_deleted=False).first()

        if user:
            # 标记用户为已删除
            user.is_deleted = True
            user.deleted_at = datetime.now()

            # 查找该用户关联的访客记录
            visitor_logs = VisitorLog.query.filter_by(visitor_phone_number=user.phone_number, is_active=True,
                                                      is_deleted=False).all()

            for visitor_log in visitor_logs:
                visitor_log.is_active = False

            # 提交数据库更新
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return format_response(False, error=f'数据库更新失败: {str(e)}'), 500

            # 从 Redis 中删除用户的 Token
            redis_client.delete(user.id)

            return format_response(True, {'message': '用户删除成功'}), 200

        return format_response(False, error='用户未找到'), 404

    @staticmethod
    def search_users(json_string, page=1, per_page=10, sort_field='id', sort_order='asc'):
        """检索用户信息"""

        # 将参数中的json字符串转换成字典
        filters = {}
        if json_string:
            try:
                filters = json.loads(json_string)  # 将字符串转换为字典
            except ValueError:
                return format_response(False, error='无效的 JSON'), 400

        # 检查 sort_field 是否是 User 模型中的有效列
        if sort_field not in User.__table__.columns:
            return format_response(False, error='无效的排序字段'), 400

        # 创建查询对象
        query = User.query.filter(User.is_deleted == False)

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
            query = query.filter(User.is_active == filters['is_active'])

        # 动态排序，确保sort_field是数据库表中的有效字段
        if sort_order.lower() == 'asc':
            query = query.order_by(asc(getattr(User, sort_field)))
        elif sort_order.lower() == 'desc':
            query = query.order_by(desc(getattr(User, sort_field)))
        else:
            # 如果排序顺序无效，则默认使用升序
            query = query.order_by(asc(getattr(User, sort_field)))

        # 分页
        paginated_users = query.paginate(page=page, per_page=per_page, error_out=False)

        # 返回分页后的数据、总页数、当前页和每页记录数
        return format_response(True, {
            "users": [user.to_dict() for user in paginated_users.items],
            "total_pages": paginated_users.pages,
            "current_page": page,
            "per_page": per_page
        }), 200
