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


class UserController:
    @staticmethod
    def get_users(page=1, per_page=10):
        """获取所有用户"""
        paginated_users = User.query.paginate(page=page, per_page=per_page, error_out=False)  # 分页
        return paginated_users.items, paginated_users.pages  # 返回分页后的数据和总页数

    @staticmethod
    def get_user_by_id(user_id):
        """根据ID获取用户"""
        return User.query.get(user_id)

    @staticmethod
    def create_user(username, phone_number, password_hash):
        """创建用户"""
        user = User(username=username, phone_number=phone_number, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def update_user(user_id, username=None, phone_number=None, password_hash):

    @staticmethod
    def delete_user(user_id):
        """删除用户"""
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False


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