# -*- coding: utf-8 -*-
"""
# 文件名称: utils/validate_utils.py
# 作者: 罗嘉淳
# 创建日期: 2024-09-27
# 版本: 1.0
# 描述: 实现了身份证、手机号的合法性验证。
"""


import re


def validate_username(username):
    # 正则表达式匹配用户名，长度为3到20个字符，由字母、数字、下划线组成
    pattern = r'^[a-zA-Z0-9_]{3,20}$'
    return bool(re.match(pattern, username))


def validate_name(name):
    # 正则表达式匹配中文或英文姓名，允许中间有连字符、空格或·符号
    pattern = r"^[\u4e00-\u9fa5]{2,10}(·[\u4e00-\u9fa5]{2,10})*$|^[a-zA-Z]+([-· ][a-zA-Z]+)*$"
    return bool(re.match(pattern, name))


def validate_gender(gender):
    # 正则表达式匹配性别
    pattern = r"^男|女$"
    return bool(re.match(pattern, gender))


def validate_id_type(id_type):
    # 正则表达式匹配证件类型
    pattern = r"^居民身份证|护照|港澳居民来往内地通行证|台湾居民来往大陆通行证$"
    return bool(re.match(pattern, id_type))


def validate_id_card(card_number):
    # 正则表达式验证身份证号格式
    pattern = r"^\d{17}[\dXx]$"
    if not re.match(pattern, card_number):
        return False

    # 加权因子和校验码对应表
    weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    check_codes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']

    # 计算校验码
    sum_val = sum(int(card_number[i]) * weights[i] for i in range(17))
    calculated_check_code = check_codes[sum_val % 11]

    return card_number[-1].upper() == calculated_check_code


def validate_passport(card_number):
    # 正则表达式验证护照的合法性
    pattern = r"^[a-zA-Z][0-9]{8}$"
    return bool(re.match(pattern, card_number))


def validate_hk_macau_pass(card_number):
    # 正则表达式验证港澳居民来往内地通行证的合法性
    pattern = r"^[HMhm][0-9]{8,10}$"
    return bool(re.match(pattern, card_number))


def validate_tw_pass(card_number):
    # 正则表达式验证台湾居民来往大陆通行证的合法性
    pattern = r"^\d{8}|\d{10}$"
    return bool(re.match(pattern, card_number))


def validate_phone_number(phone_number):
    # 正则表达式匹配手机号格式
    pattern = r"^1[3-9]\d{9}$"
    return bool(re.match(pattern, phone_number))


def validate_id_number(id_type, id_number):
    # 校验证件号码合法性
    if id_type == '居民身份证':
        return validate_id_card(id_number)
    if id_type == '护照':
        return validate_passport(id_number)
    if id_type == '港澳居民来往内地通行证':
        return validate_hk_macau_pass(id_number)
    if id_type == '台湾居民来往大陆通行证':
        return validate_tw_pass(id_number)
    return False

def validate_license_plate(license_plate):
    # 正则表达式匹配车牌格式
    pattern = (
        r"^("
        # 普通车牌（如：京A12345）
        r"[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵青藏川宁琼使领A-Z]{1}[A-Z]{1}[A-Z0-9]{5}"
        # 新能源车牌（如：京AD12345）
        r"|[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵青藏川宁琼]{1}[A-Z]{1}[DF]{1}[A-HJ-NP-Z0-9]{5}"
        # 武警车牌（如：WJ12345）
        r"|WJ[0-9]{5}"
        # 军车牌（如：军A12345）
        r"|军[A-Z]{1}[0-9]{5}"
        # 领使馆车牌（如：使12345，领12345）
        r"|使[0-9]{6}|领[0-9]{6}"
        # 警车牌（如：沪A1234警）
        r"|[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵青藏川宁琼]{1}[A-Z]{1}[0-9]{4}警"
        # 教练车牌（如：京A12345学）
        r"|[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵青藏川宁琼]{1}[A-Z]{1}[A-Z0-9]{5}学"
        # 挂车车牌（如：京A1234挂）
        r"|[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵青藏川宁琼]{1}[A-Z]{1}[0-9]{4}挂"
        r")$"
    )
    return bool(re.match(pattern, license_plate))

def validate_visit_type(visit_type):
    # 正则表达式匹配访客类型
    pattern = r"^因公访问|因私访问|社会公众$"
    return bool(re.match(pattern, visit_type))