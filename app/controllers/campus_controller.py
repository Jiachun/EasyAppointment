"""
#文件名称: controllers/campus_controller.py
#作者: 李业
#创建日期: 2024-10-01
#版本:1.0
#描述: 校区业务逻辑控制器
"""

from app.models import Campus
from extensions.db import db


class CampusController:
    @staticmethod
    def get_all_campus():
        """获取所有校区"""
        return Campus.query.all()

    @staticmethod
    def create_campus(name, description):
        """创建校区"""
        campus = Campus(name=name, description=description)
        db.session.add(campus)
        db.session.commit()
        return campus

    @staticmethod
    def get_campus(campus_id):
        """根据ID获取校区"""
        return Campus.query.get(campus_id)


    @staticmethod
    def delete_campus(campus_id):
        """删除校区"""
        campus = Campus.query.get(campus_id)
        if campus:
            db.session.delete(campus)
            db.session.commit()
            return True
        return False

