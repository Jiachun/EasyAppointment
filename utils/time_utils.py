# -*- coding: utf-8 -*-
"""
# 文件名称: utils/time_utils.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-05
# 版本: 1.0
# 描述: 实现了时间的计算和转换功能。
"""

from datetime import datetime, timedelta


def datetime_to_string(dt, fmt="%Y-%m-%d %H:%M:%S"):
    # 将 datetime 对象转换为指定格式的字符串
    return dt.strftime(fmt)


def string_to_datetime(time_str, fmt="%Y-%m-%d %H:%M:%S"):
    # 将指定格式的字符串转换为 datetime 对象
    return datetime.strptime(time_str, fmt)


def compare_time_strings(time_str1, time_str2, fmt="%Y-%m-%d %H:%M:%S"):
    # 将字符串转换为 datetime 对象进行比较
    time1 = datetime.strptime(time_str1, fmt)
    time2 = datetime.strptime(time_str2, fmt)
    return time1 > time2


def is_time_before_now(time_str, fmt="%Y-%m-%d %H:%M:%S"):
    # 计算字符串时间是否在当前时间之前
    time = datetime.strptime(time_str, fmt)
    now = datetime.now()
    return time < now


def is_time_after_now(time_str, fmt="%Y-%m-%d %H:%M:%S"):
    # 计算字符串时间是否在当前时间之后
    time = datetime.strptime(time_str, fmt)
    now = datetime.now()
    return time > now


def are_times_on_same_day(time_str1, time_str2, fmt="%Y-%m-%d %H:%M:%S"):
    # 计算两个字符串时间节点是否在同一天
    time1 = datetime.strptime(time_str1, fmt)
    time2 = datetime.strptime(time_str2, fmt)
    return time1.date() == time2.date()


def is_time_within_three_days_future(time_str, fmt="%Y-%m-%d %H:%M:%S"):
    # 计算字符串时间是否在当前时间之后的3天内
    time = datetime.strptime(time_str, fmt)
    now = datetime.now()
    three_days_future = now + timedelta(days=3)
    return three_days_future <= time <= now
