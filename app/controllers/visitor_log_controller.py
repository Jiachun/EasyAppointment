# -*- coding: utf-8 -*-
"""
# 文件名称: controllers/visitor_log_controller.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-05
# 版本: 1.0
# 描述: 访客记录逻辑控制器
"""

from datetime import datetime
from app.models import VisitorLog
from extensions.db import db
from utils.validate_utils import validate_visit_type

class VisitorLogController:
    @staticmethod
    def get_all_visitor_logs(page=1, per_page=10):
        """获取所有访客记录"""

        # 分页
        paginated_visitor_logs = VisitorLog.query.paginate(page=page, per_page=per_page, error_out=False)

        # 返回分页后的数据、总页数、当前页和每页记录数
        return {
            "visitors": [visitor_log.to_dict() for visitor_log in paginated_visitor_logs.items],
            "total_pages": paginated_visitor_logs.pages,
            "current_page": page,
            "per_page": per_page
        }, 200

    @staticmethod
    def get_visitor_log_by_id(visitor_log_id):
        """根据ID获取访客记录"""
        visitor_log = VisitorLog.query.get(visitor_log_id)
        if visitor_log:
            return visitor_log.to_dict(), 200
        return {'error': '访客记录未找到'}, 404

    @staticmethod
    def create_visitor_log(data):
        """创建访客记录"""

        # 校验访客类型，因公访问、因私访问、社会公众
        if 'visit_type' not in data:
            return {'error': '访客类型不能为空'}, 400
        if not validate_visit_type(data['visit_type']):
            return {'error': '访客类型有误'}, 400

        # 校验访问时间和离校时间
        if 'visit_time' not in data:
            return {'error': '访问时间不能为空'}, 400
        if 'leave_time' not in data:
            return {'error': '离校时间不能为空'}, 400
        

        visitor_log = VisitorLog(
            visit_type=data['visit_type'],
            visit_time=data['visit_time'],
            leave_time=data['leave_time'],
            campus=data['campus'],
            visitor_org=data.get('visitor_org', ''),
            accompanying_people=data.get('accompanying_people', ''),
            visited_person_name=data.get('visited_person_name', ''),
            visited_person_org=data.get('visited_person_org', ''),
            reason=data.get('reason', ''),
            license_plate=data.get('license_plate', ''),
            approver=None,
            is_approved=None,
            approval_time=None,
            entry_time=None,
            is_deleted=False,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        # 提交数据库更新
        try:
            db.session.add(visitor_log)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': '数据库更新失败: {}'.format(str(e))}, 500

        return visitor_log.to_dict(), 200


    @staticmethod
    def delete_user(visitor_log_id):
        """删除访客记录"""

        # 查找现有的访客记录
        visitor_log = VisitorLog.query.filter_by(id=visitor_log_id, is_deleted=False).first()

        if visitor_log:
            visitor_log.is_deleted = True

            # 提交数据库更新
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return {'error': '数据库更新失败: {}'.format(str(e))}, 500
            return {'message': '访客记录删除成功'}, 200

        return {'error': '访客记录未找到'}, 404