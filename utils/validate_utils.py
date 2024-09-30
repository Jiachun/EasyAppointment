# -*- coding: utf-8 -*-
"""
# 文件名称: utils/validate_utils.py
# 作者: 罗嘉淳
# 创建日期: 2024-09-27
# 版本: 1.0
# 描述: 实现了身份证、邮箱、手机号的合法性验证。
"""


import re
from id_validator import validator


def validate_id_card(id_card):
    # 验证身份证号合法性
    validator.is_valid(id_card)


def validate_email(email):
    # 正则表达式匹配邮箱格式
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email))


def validate_phone_number(phone_number):
    # 正则表达式匹配手机号格式
    pattern = r"^1[3-9]\d{9}$"
    return bool(re.match(pattern, phone_number))