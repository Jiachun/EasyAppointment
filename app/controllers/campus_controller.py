# -*- coding: utf-8 -*-
"""
# 文件名称: controllers/campus_controller.py
# 作者: 李业
# 创建日期: 2024-10-01
# 版本: 1.0
# 描述: 校区信息逻辑控制器
"""

from app.models import Campus
from extensions.db import db


class CampusController:
    @staticmethod
    def get_all_campuses(page=1, per_page=10):
        """获取所有校区信息"""

        # 分页
        paginated_campuses = Campus.query.paginate(page=page, per_page=per_page, error_out=False)

        # 返回分页后的数据、总页数、当前页和每页记录数
        return {
            "campuses": [campus.to_dict() for campus in paginated_campuses.items],
            "total_pages": paginated_campuses.pages,
            "current_page": page,
            "per_page": per_page
        }, 200


    @staticmethod
    def get_campus_by_id(campus_id):
        """根据ID获取校区信息"""
        campus = Campus.query.get(campus_id)
        if campus:
            return campus.to_dict(), 200
        return {'error': '校区未找到'}, 404


    @staticmethod
    def create_campus(data):
        """创建校区信息"""

        # 校验校区名称是否存在并有效
        if 'name' not in data or len(data['name']) < 3:
            return {'error': '校区名称不能为空且至少为3个字符'}, 400
        if Campus.query.filter_by(name=data['name']).first():
            return {'error': '校区名称已存在'}, 400

        campus = Campus(
            name=data['name'],
            description=data.get('description', ''),
        )

        # 提交数据库更新
        try:
            db.session.add(campus)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': '数据库更新失败: {}'.format(str(e))}, 500

        return campus.to_dict(), 200


    @staticmethod
    def update_campus(campus_id, data):
        """更新校区信息"""

        # 校验校区名称是否有效
        if 'name' not in data or len(data['name']) < 3:
            return {'error': '校区名称不能为空且至少为3个字符'}, 400
        if Campus.query.filter(Campus.name==data['name'], Campus.id!=campus_id).first():
            return {'error': '校区名称已存在'}, 400

        # 查找现有的校区信息
        campus = Campus.query.get(campus_id)
        if not campus:
            return {'error': '校区未找到'}, 404

        # 更新校区信息
        if 'name' in data:
            campus.name = data['name']
        if 'description' in data:
            campus.description = data['description']

        # 提交数据库更新
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': '数据库更新失败: {}'.format(str(e))}, 500

        return campus.to_dict(), 200


    @staticmethod
    def delete_campus(campus_id):
        """删除校区信息"""

        # 查找现有的校区信息
        campus = Campus.query.get(campus_id)

        if campus:
            # 提交数据库更新
            try:
                db.session.delete(campus)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return {'error': '数据库更新失败: {}'.format(str(e))}, 500
            return {'message': '校区删除成功'}, 200

        return {'error': '校区未找到'}, 404

