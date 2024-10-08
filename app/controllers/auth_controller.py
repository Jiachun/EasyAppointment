# -*- coding: utf-8 -*-
"""
# 文件名称: controllers/auth_controller.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-06
# 版本: 1.0
# 描述: 认证与授权逻辑控制器
"""


import requests
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from app.config import Config
from app.models import User
from extensions.db import redis_client, db
from utils.random_utils import generate_random_string
import jwt


class AuthController:
    @staticmethod
    def login(data):
        """用户登录认证"""

        # 校验用户名是否有效
        if 'username' not in data or not data['username']:
            return {'error': '请输入用户名'}, 400

        # 校验密码是否有效
        if 'password' not in data or not data['password']:
            return {'error': '请输入密码'}, 400

        username = data['username']
        password = data['password']

        # 检查用户是否被锁定
        lock_key = f"lock_{username}"
        if redis_client.get(lock_key):
            return {'error': '账户已锁定，请稍后再试'}, 403

        # 查找现有的用户信息
        user = User.query.filter_by(username=username, is_deleted=False).first()

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


    @staticmethod
    def logout(user):
        """用户注销"""
        try:
            # 从 Redis 中删除用户的 Token
            redis_client.delete(user.id)
            return {'message': '注销成功'}, 200
        except Exception as e:
            return {'error': f'注销失败: {str(e)}'}, 500

    @staticmethod
    def change_password(user, data):
        """用户修改密码"""
        # 校验新旧密码
        if 'old_password' not in data or 'new_password' not in data:
            return {'error': '请提供旧密码和新密码'}, 400

        old_password = data['old_password']
        new_password = data['new_password']

        # 校验旧密码是否正确
        if not check_password_hash(user.password_hash, old_password):
            return {'error': '旧密码不正确'}, 400

        # 更新新密码
        user.password_hash = generate_password_hash(new_password)

        # 提交数据库更新
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': '数据库更新失败: {}'.format(str(e))}, 500

        # 清除用户的 Token（要求重新登录）
        redis_client.delete(user.id)

        return {'message': '密码修改成功，请重新登录'}, 200


    @staticmethod
    def set_password(data):
        """管理员修改用户密码"""

        # 获取用户ID和新密码
        user_id = data['user_id']
        new_password = data['new_password']

        # 校验传入的数据是否完整
        if not user_id or not new_password:
            return {'error': '用户ID和新密码不能为空'}, 400

        # 查找目标用户
        user = User.query.filter_by(id=user_id, is_deleted=False).first()
        if not user:
            return {'error': '用户不存在'}, 403

        # 设置新密码
        user.password_hash = generate_password_hash(new_password)

        # 提交数据库更新
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': '数据库更新失败: {}'.format(str(e))}, 500

        # 清除用户的 Token（要求重新登录）
        redis_client.delete(user.id)

        return {'message': '密码已成功更新'}, 200


    @staticmethod
    def wechat_login(data):
        """微信用户登录"""

        # 获取code
        if 'code' not in data or not data['code']:
            return {'error': '缺少 code 参数'}, 400

        code = data['code']

        # 微信小程序的 AppID 和 AppSecret
        app_id = Config.WECHAT_APP_ID
        app_secret = Config.WECHAT_APP_SECRET

        # 向微信服务器发送请求，获取 openid 和 session_key
        url = f"https://api.weixin.qq.com/sns/jscode2session?appid={app_id}&secret={app_secret}&js_code={code}&grant_type=authorization_code"
        response = requests.get(url)
        data = response.json()

        if 'openid' not in data or not data['openid']:
            return {'error': '无法获取 openid'}, 400

        openid = data['openid']

        # 在数据库中检查用户是否已注册
        user = User.query.filter_by(openid=openid, is_deleted=False).first()

        if not user:
            # 如果用户不存在
            return {'error': '用户尚未绑定'}, 403

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


    @staticmethod
    def bind_user(data):
        """绑定用户"""

        # 验证用户的手机号是否正确
        if 'phone_number' not in data or not data['phone_number']:
            return {'error': '手机号码不能为空'}, 400

        # 获取code
        if 'code' not in data or not data['code']:
            return {'error': '缺少 code 参数'}, 400

        code = data['code']

        # 微信小程序的 AppID 和 AppSecret
        app_id = Config.WECHAT_APP_ID
        app_secret = Config.WECHAT_APP_SECRET

        # 向微信服务器发送请求，获取 openid 和 session_key
        url = f"https://api.weixin.qq.com/sns/jscode2session?appid={app_id}&secret={app_secret}&js_code={code}&grant_type=authorization_code"
        response = requests.get(url)
        data = response.json()

        if 'openid' not in data or not data['openid']:
            return {'error': '无法获取 openid'}, 400

        openid = data['openid']

        # 查找手机号码绑定的用户
        user = User.query.filter_by(phone_number=data['phone_number'], is_deleted=False).first()

        try:
            if user:
                # 如果用户存在，绑定openid
                user.openid = openid
            else:
                # 如果用户不存在，创建用户
                user = User(
                    username=generate_random_string(),
                    password=generate_password_hash(generate_random_string()),
                    phone_number=data['phone_number'],
                    openid=openid,
                )
                db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': '数据库更新失败: {}'.format(str(e))}, 500

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


    @staticmethod
    def unbind_user(data):
        """解绑用户"""

        # 校验 openid 是否为空
        if 'openid' not in data or not data['openid']:
            return {'error': '缺少 openid 参数'}, 400

        # 查找用户并解绑
        user = User.query.filter_by(openid=data['openid'], is_deleted=False).first()

        if not user:
            return {'error': '用户不存在'}, 400

        # 清除 openid
        user.openid = None

        # 提交数据库更新
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': '数据库更新失败: {}'.format(str(e))}, 500

        # 清除用户的 Token（要求重新登录）
        redis_client.delete(user.id)

        return {'message': '用户解绑成功'}, 200