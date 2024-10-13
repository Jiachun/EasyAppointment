# -*- coding: utf-8 -*-
"""
# 文件名称: utils/format_utils.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-13
# 版本: 1.0
# 描述: 实现了格式化返回值功能。
"""


def format_response(success, data=None, error=None):
    response = {'success': success}
    if success and data is not None:
        response['data'] = data
    if not success and error is not None:
        response['error'] = error
    return response