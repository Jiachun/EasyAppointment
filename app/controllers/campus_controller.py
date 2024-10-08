# -*- coding: utf-8 -*-
"""
# 文件名称: controllers/campus_controller.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-10
# 版本: 1.0
# 描述: 校区信息逻辑控制器
"""


from app.models import Campus
from extensions.db import db
from datetime import datetime
from sqlalchemy import asc, desc
import json


class CampusController:
    @staticmethod
    def get_all_campuses(page=1, per_page=10):
        """获取所有校区信息"""

        # 分页
        paginated_campuses = Campus.query.filter_by(is_deleted=False).paginate(page=page, per_page=per_page, error_out=False)

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
        campus = Campus.query.filter_by(id=campus_id, is_deleted=False).first()
        if campus:
            return campus.to_dict(), 200
        return {'error': '校区未找到'}, 404


    @staticmethod
    def create_campus(data):
        """创建校区信息"""

        # 校验校区名称是否存在并有效
        if 'name' not in data or not data['name'] or len(data['name']) < 3:
            return {'error': '校区名称不能为空且至少为3个字符'}, 400
        if Campus.query.filter_by(name=data['name'], is_deleted=False).first():
            return {'error': '校区名称已存在'}, 400

        campus = Campus(
            name=data['name'],
            description=data.get('description') or '',
            is_deleted=False,
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
        if 'name' not in data or not data['name'] or len(data['name']) < 3:
            return {'error': '校区名称不能为空且至少为3个字符'}, 400
        if Campus.query.filter(Campus.name==data['name'], Campus.id!=campus_id, Campus.is_deleted==False).first():
            return {'error': '校区名称已存在'}, 400

        # 查找现有的校区信息
        campus = Campus.query.filter_by(id=campus_id, is_deleted=False).first()
        if not campus:
            return {'error': '校区未找到'}, 404

        # 更新校区信息
        if 'name' in data:
            campus.name = data['name']
        if 'description' in data:
            campus.description = data.get('description') or ''

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
        campus = Campus.query.filter_by(id=campus_id, is_deleted=False).first()

        if campus:
            campus.is_deleted = True
            campus.deleted_at = datetime.now()

            # 提交数据库更新
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return {'error': '数据库更新失败: {}'.format(str(e))}, 500
            return {'message': '校区删除成功'}, 200

        return {'error': '校区未找到'}, 404


    @staticmethod
    def search_campuses(json_string, page=1, per_page=10, sort_field='id', sort_order='asc'):
        """检索校区信息"""

        # 将参数中的json字符串转换成字典
        filters = {}
        if json_string:
            try:
                filters = json.loads(json_string)  # 将字符串转换为字典
            except ValueError:
                return {"error": "无效的 JSON"}, 400

        # 检查 sort_field 是否是 Campus 模型中的有效列
        if sort_field not in Campus.__table__.columns:
            return {'error': '无效的排序字段'}, 400

        # 创建查询对象
        query = Campus.query.filter(Campus.is_deleted==False)

        # 如果有校区名称的条件
        if filters.get('name'):
            query = query.filter(Campus.name.contains(filters['name']))

        # 动态排序，确保sort_field是数据库表中的有效字段
        if sort_order.lower() == 'asc':
            query = query.order_by(asc(getattr(Campus, sort_field)))
        elif sort_order.lower() == 'desc':
            query = query.order_by(desc(getattr(Campus, sort_field)))
        else:
            # 如果排序顺序无效，则默认使用升序
            query = query.order_by(asc(getattr(Campus, sort_field)))

        # 分页
        paginated_campuses = query.paginate(page=page, per_page=per_page, error_out=False)

        # 返回分页后的数据、总页数、当前页和每页记录数
        return {
            "campuses": [campus.to_dict() for campus in paginated_campuses.items],
            "total_pages": paginated_campuses.pages,
            "current_page": page,
            "per_page": per_page
        }, 200