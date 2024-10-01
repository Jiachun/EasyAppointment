# -*- coding: utf-8 -*-
"""
# 文件名称: controllers/campus_controller.py
# 作者: 李业
# 创建日期: 2024-10-01
# 版本: 1.0
# 描述: 校区业务逻辑控制器
"""

from app.models import Campus
from extensions.db import db


class CampusController:
    @staticmethod
    def get_all_campuses(page=1, per_page=10):
        """获取所有校区"""
        paginated_campuses = Campus.query.paginate(page=page, per_page=per_page, error_out=False)  # 分页
        return paginated_campuses.items, paginated_campuses.pages  # 返回分页后的数据和总页数

    @staticmethod
    def get_campus_by_id(campus_id):
        """根据ID获取校区"""
        return Campus.query.get(campus_id)

    @staticmethod
    def create_campus(name, description):
        """创建校区"""
        campus = Campus(name=name, description=description)
        db.session.add(campus)
        db.session.commit()
        return campus

    @staticmethod
    def update_campus(campus_id, **kwargs):
        """更新校区"""
        campus = Campus.query.get(campus_id)
        if not campus:
            return None

        for key, value in kwargs.items():
            if hasattr(campus, key):
                setattr(campus, key, value)

        db.session.commit()
        return campus

    @staticmethod
    def delete_campus(campus_id):
        """删除校区"""
        campus = Campus.query.get(campus_id)
        if campus:
            db.session.delete(campus)
            db.session.commit()
            return True
        return False

