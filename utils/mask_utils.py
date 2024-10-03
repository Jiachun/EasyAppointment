# -*- coding: utf-8 -*-
"""
# 文件名称: utils/mask_utils.py
# 作者: 罗嘉淳
# 创建日期: 2024-09-27
# 版本: 1.0
# 描述: 实现了敏感数据的脱敏。
"""


def mask_name(name):
    # 姓名脱敏
    if len(name) == 2:
        return name[0] + '*'
    elif len(name) >= 3:
        return name[0] + '*' * (len(name) - 2) + name[-1]


def mask_id_card(id_card):
    # 身份证脱敏
    return id_card[:6] + '********' + id_card[-4:]


def mask_phone_number(phone_number):
    # 手机号脱敏
    return phone_number[:3] + '****' + phone_number[-4:]