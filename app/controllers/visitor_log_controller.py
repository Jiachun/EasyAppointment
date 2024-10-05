# -*- coding: utf-8 -*-
"""
# 文件名称: controllers/visitor_log_controller.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-05
# 版本: 1.0
# 描述: 访客记录逻辑控制器
"""

from datetime import datetime
from app.models import VisitorLog, Campus, Department
from extensions.db import db
from utils.validate_utils import validate_visit_type, validate_name, validate_license_plate
from utils.time_utils import compare_time_strings, is_time_before_now, is_time_within_three_days_future, are_times_on_same_day

class VisitorLogController:
    @staticmethod
    def get_all_visitor_logs(page=1, per_page=10):
        """获取所有访客记录"""

        # 分页
        paginated_visitor_logs = VisitorLog.query.filter_by(is_deleted=False).paginate(page=page, per_page=per_page, error_out=False)

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
        visitor_log = VisitorLog.query.filter_by(id=visitor_log_id, is_deleted=False).first()
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
        if compare_time_strings(data['visit_time'], data['leave_time']):
            return {'error': '离校时间不能早于访问时间'}, 400
        if is_time_before_now(data['visit_time']):
            return {'error': '访问时间不能早于当前时间'}, 400
        if not are_times_on_same_day(data['visit_time'], data['leave_time']):
            return {'error': '访问时间和离校时间必须是同一天'}, 400
        if not is_time_within_three_days_future(data['visit_time']):
            return {'error': '当前时间段未开放预约'}, 400

        # 校验校区名称
        if 'campus' not in data:
            return {'error': '校区名称不能为空'}, 400
        if not Campus.query.filter_by(name=data['campus']).first():
            return {'error': '校区名称有误'}, 400

        if not data['visit_type'] == '社会公众':

            # 校验访客所属单位
            if data['visit_type'] == '因公访问' and 'visitor_org' not in data:
                return {'error': '访客所属单位不能为空'}, 400

            # 校验被访人姓名格式
            if 'visited_person_name' not in data:
                return {'error': '被访人姓名不能为空'}, 400
            if validate_name(data['visited_person_name']):
                return {'error': '被访人姓名格式有误'}, 400

            # 校验被访人部门
            if 'visited_person_org' not in data:
                return {'error': '被访人部门不能为空'}, 400
            if not Department.query.filter_by(name=data['visited_person_org']).first():
                return {'error': '被访人部门名称有误'}, 400

            # 校验访问事由
            if 'reason' not in data or len(data['reason']) < 2:
                return {'error': '访问事由不能为空且至少为2个字符'}, 400

            # 校验车牌格式
            if 'license_plate' in data and not validate_license_plate(data['license_plate']):
                return {'error': '车牌格式有误'}, 400


        visitor_log = VisitorLog(
            visit_type=data['visit_type'],
            visit_time=data['visit_time'],
            leave_time=data['leave_time'],
            campus=data['campus'],
            visitor_org=data.get('visitor_org', ''),
            visited_person_name=data.get('visited_person_name', ''),
            visited_person_org=data.get('visited_person_org', ''),
            reason=data.get('reason', ''),
            accompanying_people=data.get('accompanying_people', ''),
            license_plate=data.get('license_plate', ''),
            approver=None,
            is_approved=None,
            approval_time=None,
            entry_time=None,
            is_cancelled=False,
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
    def update_visitor_log(visitor_log_id, data):
        """更新访客记录"""

        # 查找现有的访客记录
        visitor_log = VisitorLog.query.filter_by(id=visitor_log_id, is_deleted=False).first()
        if not visitor_log:
            return {'error': '访客记录未找到'}, 404

        # 已审批的访客记录无法修改
        if visitor_log.is_approved is not None:
            return {'error': '已审批的访客记录无法修改'}, 400

        # 已取消的访客记录无法修改
        if visitor_log.is_cancelled:
            return {'error': '已取消的访客记录无法修改'}, 400

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
        if compare_time_strings(data['visit_time'], data['leave_time']):
            return {'error': '离校时间不能早于访问时间'}, 400
        if is_time_before_now(data['visit_time']):
            return {'error': '访问时间不能早于当前时间'}, 400
        if not are_times_on_same_day(data['visit_time'], data['leave_time']):
            return {'error': '访问时间和离校时间必须是同一天'}, 400
        if not is_time_within_three_days_future(data['visit_time']):
            return {'error': '当前时间段未开放预约'}, 400

        # 校验校区名称
        if 'campus' not in data:
            return {'error': '校区名称不能为空'}, 400
        if not Campus.query.filter_by(name=data['campus']).first():
            return {'error': '校区名称有误'}, 400

        if not data['visit_type'] == '社会公众':

            # 校验访客所属单位
            if data['visit_type'] == '因公访问' and 'visitor_org' not in data:
                return {'error': '访客所属单位不能为空'}, 400

            # 校验被访人姓名格式
            if 'visited_person_name' not in data:
                return {'error': '被访人姓名不能为空'}, 400
            if validate_name(data['visited_person_name']):
                return {'error': '被访人姓名格式有误'}, 400

            # 校验被访人部门
            if 'visited_person_org' not in data:
                return {'error': '被访人部门不能为空'}, 400
            if not Department.query.filter_by(name=data['visited_person_org']).first():
                return {'error': '被访人部门名称有误'}, 400

            # 校验访问事由
            if 'reason' not in data or len(data['reason']) < 2:
                return {'error': '访问事由不能为空且至少为2个字符'}, 400

            # 校验车牌格式
            if 'license_plate' in data and not validate_license_plate(data['license_plate']):
                return {'error': '车牌格式有误'}, 400

        visitor_log.visit_type = data['visit_type']
        visitor_log.visit_time = data['visit_time']
        visitor_log.leave_time = data['leave_time']
        visitor_log.campus = data['campus']
        visitor_log.visitor_org = data.get('visitor_org', '')
        visitor_log.visited_person_name = data.get('visited_person_name', '')
        visitor_log.visited_person_org = data.get('visited_person_org', '')
        visitor_log.reason = data.get('reason', '')
        visitor_log.accompanying_people = data.get('accompanying_people', '')
        visitor_log.license_plate = data.get('license_plate', '')
        visitor_log.update_time = datetime.now()

        # 提交数据库更新
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': '数据库更新失败: {}'.format(str(e))}, 500

        return visitor_log.to_dict(), 200


    @staticmethod
    def delete_visitor_log(visitor_log_id):
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