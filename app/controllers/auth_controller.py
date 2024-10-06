# -*- coding: utf-8 -*-
"""
# 文件名称: controllers/auth_controller.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-06
# 版本: 1.0
# 描述: 认证与授权逻辑控制器
"""


from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from app.config import Config
from app.models import User
from extensions.db import redis_client
import jwt


class AuthController:
    @staticmethod
    def login(data):
        """用户登录认证"""

        # 校验用户名是否有效
        if 'username' not in data:
            return {'error': '请输入用户名'}, 400

        # 校验密码是否有效
        if 'password' not in data:
            return {'error': '请输入密码'}, 400

        username = data['username']
        password = data['password']

        # 检查用户是否被锁定
        lock_key = f"lock_{username}"
        if redis_client.get(lock_key):
            return {'error': '账户已锁定，请稍后再试'}, 403

        # 查找现有的用户信息
        user = User.query.filter_by(username=username).first()

        # 校验用户名和密码是否正确
        if user and check_password_hash(user.password_hash, password):
            # 清除失败次数
            redis_client.delete(f"login_attempts_{username}")

            # 生成 token
            now = datetime.now()
            token = jwt.encode(
                {
                    'id': user.id,
                    'exp': now + timedelta(seconds=Config.TOKEN_EXPIRY),
                    'refresh_time': now + timedelta(seconds=Config.TOKEN_EXPIRY - Config.REFRESH_THRESHOLD)
                },
                Config.JWT_SECRET_KEY, algorithm="HS256"
            )

            # 将 Token 存入 Redis
            redis_client.set(user.id, token, ex=Config.TOKEN_EXPIRY)
            return {'token': token}, 200

        # 登录失败，记录失败次数
        attempts_key = f"login_attempts_{username}"
        attempts = redis_client.get(attempts_key)

        if attempts:
            attempts = int(attempts)
            if attempts + 1 >= Config.MAX_LOGIN_ATTEMPTS:
                # 锁定账户
                redis_client.set(lock_key, "locked", ex=Config.LOCK_TIME)
                return {'error': '账户已锁定，请稍后再试'}, 403
            else:
                redis_client.incr(attempts_key)
        else:
            redis_client.set(attempts_key, 1, ex=Config.LOCK_TIME)

        return {'error': '用户名或密码错误'}, 401