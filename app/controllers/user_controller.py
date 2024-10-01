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
    def get_all_users():
        """获取所有用户"""
        return User.query.all()

    @staticmethod
    def create_user(username, email, password_hash):
        """创建用户"""
        user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_user_by_id(user_id):
        """根据ID获取用户"""
        return User.query.get(user_id)

    @staticmethod
    def delete_user(user_id):
        """删除用户"""
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False
