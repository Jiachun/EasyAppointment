# -*- coding: utf-8 -*-
"""
# 文件名称: utils/token_decorator.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-07
# 版本: 1.0
# 描述: Token 验证装饰器。
"""

from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask import jsonify, request

from app.config import Config
from app.models import User
from extensions.db import redis_client
from utils.format_utils import format_response


def token_required(f):
    """Token 验证装饰器"""

    @wraps(f)
    def wrapper(*args, **kwargs):
        # 从请求头获取 Token
        token = request.headers.get('Authorization')

        if not token:
            # 如果请求头中没有 Token，返回 403 错误
            return jsonify(format_response(False, error='Token 丢失')), 403

        try:
            # 解码 Token，验证其有效性
            data = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['id'], is_deleted=False).first()

            if not current_user:
                # 如果没有找到对应的用户，返回 403 错误
                return jsonify(format_response(False, error='用户不存在')), 403

            # 从 Redis 获取当前用户的 Token，并与请求中的 Token 对比
            stored_token = redis_client.get(current_user.id)
            if stored_token != token:
                # 如果 Redis 中存储的 Token 与请求中的 Token 不一致，返回 403 错误
                return jsonify(format_response(False, error='Token 已失效')), 403

            # 获取当前时间和刷新时间
            now = datetime.now()
            refresh_time = datetime.fromtimestamp(data['refresh_time'])

            # 如果当前时间超过了刷新时间，则生成新的 Token
            if now > refresh_time:
                new_token = jwt.encode(
                    {
                        'id': current_user.id,
                        'exp': now + timedelta(seconds=Config.TOKEN_EXPIRY),
                        'refresh_time': now + timedelta(seconds=Config.TOKEN_EXPIRY - Config.REFRESH_THRESHOLD)
                    },
                    Config.SECRET_KEY, algorithm="HS256"
                )
                # 将新的 Token 存入 Redis 中，并设置过期时间
                redis_client.set(current_user.id, new_token, ex=Config.TOKEN_EXPIRY)
                return jsonify({'new_token': new_token}), 200

        # 捕获 Token 过期异常
        except jwt.ExpiredSignatureError:
            return jsonify(format_response(False, error='Token 已过期')), 403
        except jwt.InvalidTokenError:
            return jsonify(format_response(False, error='无效的 Token')), 403

        # 如果 Token 验证通过，调用被装饰的函数
        return f(current_user, *args, **kwargs)

    # 返回装饰器函数
    return wrapper
