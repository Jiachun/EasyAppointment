# -*- coding: utf-8 -*-
"""
# 文件名称: controllers/visitor_log_user_controller.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-11
# 版本: 1.0
# 描述: 普通用户的预约记录逻辑控制器
"""


from app.models import VisitorLog, Campus, Department
from extensions.db import db
from datetime import datetime
from sqlalchemy import desc
from utils.validate_utils import validate_visit_type, validate_name, validate_license_plate
from utils.time_utils import compare_time_strings, is_time_before_now, is_time_within_three_days_future, are_times_on_same_day


class VisitorLogUserController:
    @staticmethod
    def get_all_visitor_logs(user, page=1, per_page=10, status='all'):
        """获取该用户所有预约记录"""

        # 创建查询对象
        query = VisitorLog.query.filter(VisitorLog.visitor_phone_number == user.phone_number, VisitorLog.is_deleted == False, VisitorLog.is_active == True)

        # 按照状态检索预约记录
        if status.lower() == 'wait':
            query = query.filter(VisitorLog.is_approved.is_(None), VisitorLog.is_cancelled == False)
        elif status.lower() == 'allow':
            query = query.filter(VisitorLog.is_approved == True)
        elif status.lower() == 'deny':
            query = query.filter(VisitorLog.is_approved == False)
        elif status.lower() == 'cancel':
            query = query.filter(VisitorLog.is_cancelled == True)

        # 分页
        paginated_visitor_logs = query.order_by(desc(VisitorLog.create_time)).paginate(page=page, per_page=per_page, error_out=False)

        # 返回分页后的数据、总页数、当前页和每页记录数
        return {
            "visitor_logs": [visitor_log.to_mask() for visitor_log in paginated_visitor_logs.items],
            "total_pages": paginated_visitor_logs.pages,
            "current_page": page,
            "per_page": per_page
        }, 200


    @staticmethod
    def get_visitor_log_by_id(user, visitor_log_id):
        """根据ID获取预约记录"""
        visitor_log = VisitorLog.query.filter_by(id=visitor_log_id, visitor_phone_number=user.phone_number, is_deleted=False, is_active=True).first()
        if visitor_log:
            return visitor_log.to_mask(), 200
        return {'error': '预约记录未找到'}, 404


    @staticmethod
    def create_visitor_log(user, data):
        """创建预约记录"""

        # 校验访客类型，因公访问、因私访问、社会公众
        if 'visit_type' not in data or not data['visit_type']:
            return {'error': '访客类型不能为空'}, 400
        if not validate_visit_type(data['visit_type']):
            return {'error': '访客类型有误'}, 400

        # 校验访问时间和离校时间
        if 'visit_time' not in data or not data['visit_time']:
            return {'error': '访问时间不能为空'}, 400
        if 'leave_time' not in data or not data['leave_time']:
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
        if 'campus' not in data or not data['campus']:
            return {'error': '校区名称不能为空'}, 400
        if not Campus.query.filter_by(name=data['campus']).first():
            return {'error': '校区名称有误'}, 400

        if not data['visit_type'] == '社会公众':

            # 校验访客所属单位
            if data['visit_type'] == '因公访问' and 'visitor_org' not in data or not data['visitor_org']:
                return {'error': '访客所属单位不能为空'}, 400

            # 校验被访人姓名格式
            if 'visited_person_name' not in data or not data['visited_person_name']:
                return {'error': '被访人姓名不能为空'}, 400
            if validate_name(data['visited_person_name']):
                return {'error': '被访人姓名格式有误'}, 400

            # 校验被访人部门
            if 'visited_person_org' not in data or not data['visited_person_org']:
                return {'error': '被访人部门不能为空'}, 400
            if not Department.query.filter_by(name=data['visited_person_org']).first():
                return {'error': '被访人部门名称有误'}, 400

            # 校验访问事由
            if 'reason' not in data or not data['reason'] or len(data['reason']) < 2:
                return {'error': '访问事由不能为空且至少为2个字符'}, 400

            # 校验车牌格式
            if 'license_plate' in data:
                if not data['license_plate'] or not validate_license_plate(data['license_plate']):
                    return {'error': '车牌格式有误'}, 400

        visitor_log = VisitorLog(
            visit_type=data['visit_type'],
            visit_time=data['visit_time'],
            leave_time=data['leave_time'],
            campus=data['campus'],
            visitor_name=user.name,
            visitor_gender=user.gender,
            visitor_phone_number=user.phone_number,
            visitor_id_type=user.id_type,
            visitor_id_number=user.id_number,
            visitor_org=data.get('visitor_org') or '',
            visited_person_name=data.get('visited_person_name') or '',
            visited_person_org=data.get('visited_person_org') or '',
            reason=data.get('reason') or '',
            accompanying_people=data.get('accompanying_people') or '',
            license_plate=data.get('license_plate') or '',
            approver=None,
            is_approved=None,
            approval_time=None,
            entry_time=None,
            is_cancelled=False,
            is_active=True,
            is_deleted=False,
        )

        # 提交数据库更新
        try:
            db.session.add(visitor_log)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': '数据库更新失败: {}'.format(str(e))}, 500

        return visitor_log.to_mask(), 200


    @staticmethod
    def update_visitor_log(user, visitor_log_id, data):
        """更新预约记录"""

        # 查找现有的访客记录
        visitor_log = VisitorLog.query.filter_by(id=visitor_log_id, visitor_phone_number=user.phone_number,
                                                 is_deleted=False, is_active=True).first()

        if not visitor_log:
            return {'error': '预约记录未找到'}, 404

        # 已审批的访客记录无法修改
        if visitor_log.is_approved is not None:
            return {'error': '已审批的预约记录无法修改'}, 400

        # 已取消的访客记录无法修改
        if visitor_log.is_cancelled:
            return {'error': '已取消的预约记录无法修改'}, 400

        # 校验访客类型，因公访问、因私访问、社会公众
        if 'visit_type' not in data or not data['visit_type']:
            return {'error': '访客类型不能为空'}, 400
        if not validate_visit_type(data['visit_type']):
            return {'error': '访客类型有误'}, 400

        # 校验访问时间和离校时间
        if 'visit_time' not in data or not data['visit_time']:
            return {'error': '访问时间不能为空'}, 400
        if 'leave_time' not in data or not data['leave_time']:
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
        if 'campus' not in data or not data['campus']:
            return {'error': '校区名称不能为空'}, 400
        if not Campus.query.filter_by(name=data['campus']).first():
            return {'error': '校区名称有误'}, 400

        if not data['visit_type'] == '社会公众':

            # 校验访客所属单位
            if data['visit_type'] == '因公访问' and 'visitor_org' not in data or not data['visitor_org']:
                return {'error': '访客所属单位不能为空'}, 400

            # 校验被访人姓名格式
            if 'visited_person_name' not in data or not data['visited_person_name']:
                return {'error': '被访人姓名不能为空'}, 400
            if validate_name(data['visited_person_name']):
                return {'error': '被访人姓名格式有误'}, 400

            # 校验被访人部门
            if 'visited_person_org' not in data or not data['visited_person_org']:
                return {'error': '被访人部门不能为空'}, 400
            if not Department.query.filter_by(name=data['visited_person_org']).first():
                return {'error': '被访人部门名称有误'}, 400

            # 校验访问事由
            if 'reason' not in data or not data['reason'] or len(data['reason']) < 2:
                return {'error': '访问事由不能为空且至少为2个字符'}, 400

            # 校验车牌格式
            if 'license_plate' in data:
                if not data['license_plate'] or not validate_license_plate(data['license_plate']):
                    return {'error': '车牌格式有误'}, 400

        visitor_log.visit_type = data['visit_type']
        visitor_log.visit_time = data['visit_time']
        visitor_log.leave_time = data['leave_time']
        visitor_log.campus = data['campus']
        visitor_log.visitor_name = user.name,
        visitor_log.visitor_gender = user.gender,
        visitor_log.visitor_phone_number = user.phone_number,
        visitor_log.visitor_id_type = user.id_type,
        visitor_log.visitor_id_number = user.id_number,
        visitor_log.visitor_org = data.get('visitor_org') or ''
        visitor_log.visited_person_name = data.get('visited_person_name') or ''
        visitor_log.visited_person_org = data.get('visited_person_org') or ''
        visitor_log.reason = data.get('reason') or ''
        visitor_log.accompanying_people = data.get('accompanying_people') or ''
        visitor_log.license_plate = data.get('license_plate') or ''
        visitor_log.update_time = datetime.now()

        # 提交数据库更新
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': '数据库更新失败: {}'.format(str(e))}, 500

        return visitor_log.to_mask(), 200


    @staticmethod
    def cancel_visitor_log(user, visitor_log_id):
        """取消预约记录"""

        # 查找现有的预约记录
        visitor_log = VisitorLog.query.filter_by(id=visitor_log_id, visitor_phone_number=user.phone_number,
                                                 is_deleted=False, is_active=True).first()

        if not visitor_log:
            return {'error': '预约记录未找到'}, 404

        # 已审批的预约记录无法取消
        if visitor_log.is_approved is not None:
            return {'error': '已审批的预约记录无法修改'}, 400

        # 已取消的访客记录无法再次取消
        if visitor_log.is_cancelled:
            return {'error': '该预约记录已经取消'}, 400

        visitor_log.is_cancelled = True
        visitor_log.cancelled_at = datetime.now()

        # 提交数据库更新
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': '数据库更新失败: {}'.format(str(e))}, 500
        return {'message': '预约记录取消成功'}, 200