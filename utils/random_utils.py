# -*- coding: utf-8 -*-
"""
# 文件名称: utils/random_utils.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-07
# 版本: 1.0
# 描述: 实现了随机数据的生成。
"""


import random
import string


def generate_random_string(length=20):
    # 字符集：包含大小写字母、数字、下划线
    characters = string.ascii_letters + string.digits + '_'

    # 随机选择字符并生成指定长度的字符串
    username = ''.join(random.choices(characters, k=length))

    return username