# -*- coding: utf-8 -*-
"""
# 文件名称: controllers/user_profile_controller.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-10
# 版本: 1.0
# 描述: 用户个人信息逻辑控制器
"""


from extensions.db import db
from utils.validate_utils import validate_name, validate_gender, validate_id_type, validate_id_number


class UserProfileController:
    @staticmethod
    def get_user_profile(user):
        """获取当前用户个人信息"""
        return user.to_mask(), 200


    @staticmethod
    def update_user_profile(user, data):
        """更新当前用户个人信息"""

        # 校验姓名格式是否正确
        if 'name' not in data or not data['name']:
            return {'error': '姓名不能为空'}, 400
        if not validate_name(data['name']):
            return {'error': '姓名格式有误'}, 400

        # 校验性别格式是否正确
        if 'gender' not in data or not data['gender']:
            return {'error': '性别不能为空'}, 400
        if not validate_gender(data['gender']):
            return {'error': '性别格式有误'}, 400

        # 校验证件类型是否正确
        if 'id_type' not in data or not data['id_type']:
            return {'error': '证件类型不能为空'}, 400
        if not validate_id_type(data['id_type']):
            return {'error': '证件类型有误'}, 400

        # 校验证件号码是否合法
        if 'id_number' not in data or not data['id_number']:
            return {'error': '证件号码不能为空'}, 400
        if not validate_id_number(data['id_type'], data['id_number']):
            return {'error': '证件号码不合法'}, 400

        user.name = data['name']
        user.gender = data['gender']
        user.id_type = data['id_type']
        user.id_number = data['id_number']

        # 提交数据库更新
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': '数据库更新失败: {}'.format(str(e))}, 500

        return user.to_mask(), 200