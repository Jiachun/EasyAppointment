# -*- coding: utf-8 -*-
"""
# 文件名称: utils/mask_utils.py
# 作者: 罗嘉淳
# 创建日期: 2024-09-27
# 版本: 1.0
# 描述: 实现了敏感数据的脱敏功能。
"""


def mask_name(name):
    # 姓名脱敏
    if not name:
        return ''
    if len(name) == 2:
        return name[0] + '*'
    elif len(name) >= 3:
        return name[0] + '*' * (len(name) - 2) + name[-1]


def mask_id_number(id_number):
    # 证件号码脱敏
    return id_number[:2] + '*' * (len(id_number) - 4) + id_number[-2:]


def mask_phone_number(phone_number):
    # 手机号脱敏
    return phone_number[:2] + '*' * (len(phone_number) - 7) + phone_number[-2:]


def mask_org_name(org_name):
    # 单位名称脱敏
    if not org_name:
        return ''
    if len(org_name) == 2:
        return org_name[0] + '*'
    elif len(org_name) >= 3:
        return org_name[0] + '*' * (len(org_name) - 2) + org_name[-1]
