# -*- coding: utf-8 -*-
"""
# 文件名称: controllers/visitor_log_admin_controller.py
# 作者: 罗嘉淳
# 创建日期: 2024-10-05
# 版本: 1.0
# 描述: 管理员的访客记录逻辑控制器
"""


from app.models import VisitorLog, Campus, Department, User
from extensions.db import db
from datetime import datetime
from sqlalchemy import asc, desc
import json
from utils.validate_utils import validate_visit_type, validate_name, validate_license_plate, validate_gender, validate_id_type, validate_id_number, validate_phone_number
from utils.time_utils import compare_time_strings, is_time_before_now, is_time_within_three_days_future, are_times_on_same_day, string_to_datetime, datetime_to_string, is_time_after_now


class VisitorLogAdminController:
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

        # 校验证件类型是否正确
        if 'visitor_id_type' not in data or not data['visitor_id_type']:
            return {'error': '访客证件类型不能为空'}, 400
        if not validate_id_type(data['visitor_id_type']):
            return {'error': '访客证件类型有误'}, 400

        # 校验证件号码是否有效
        if 'visitor_id_number' not in data or not data['visitor_id_number']:
            return {'error': '访客证件号码不能为空'}, 400
        if not validate_id_number(data['visitor_id_type'], data['visitor_id_number']):
            return {'error': '访客证件号码不合法'}, 400

        # 校验手机号码是否有效
        if 'visitor_phone_number' not in data or not data['visitor_phone_number']:
            return {'error': '访客手机号码不能为空'}, 400
        if not validate_phone_number(data['visitor_phone_number']):
            return {'error': '访客手机号码格式有误'}, 400

        # 校验用户是否存在
        if not User.query.filter_by(id_number=data['visitor_id_number'], phone_number=data['visitor_phone_number'], is_deleted=False).first():
            return {'error': '该用户不存在'}, 400

        # 校验访客姓名格式是否正确
        if 'visitor_name' not in data or not data['visitor_name']:
            return {'error': '访客姓名不能为空'}, 400
        if not validate_name(data['visitor_name']):
            return {'error': '访客姓名格式有误'}, 400

        # 校验访客性别是否正确
        if 'visitor_gender' not in data or not data['visitor_gender']:
            return {'error': '访客性别不能为空'}, 400
        if not validate_gender(data['visitor_gender']):
            return {'error': '访客性别格式有误'}, 400

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
            visitor_name=data['visitor_name'],
            visitor_gender=data['visitor_gender'],
            visitor_phone_number=data['visitor_phone_number'],
            visitor_id_type=data['visitor_id_type'],
            visitor_id_number=data['visitor_id_number'],
            visitor_org=data.get('visitor_org') or '',
            visited_person_name=data.get('visited_person_name') or '',
            visited_person_org=data.get('visited_person_org') or '',
            reason=data.get('reason') or '',
            accompanying_people=data.get('accompanying_people') or '',
            license_plate=data.get('license_plate') or '',
            is_approved=None,
            approval_note=None,
            approver=None,
            approved_at=None,
            entry_time=None,
            is_cancelled=False,
            cancelled_at=None,
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

        # 校验证件类型是否正确
        if 'visitor_id_type' not in data or not data['visitor_id_type']:
            return {'error': '访客证件类型不能为空'}, 400
        if not validate_id_type(data['visitor_id_type']):
            return {'error': '访客证件类型有误'}, 400

        # 校验证件号码是否有效
        if 'visitor_id_number' not in data or not data['visitor_id_number']:
            return {'error': '访客证件号码不能为空'}, 400
        if not validate_id_number(data['visitor_id_type'], data['visitor_id_number']):
            return {'error': '访客证件号码不合法'}, 400

        # 校验手机号码是否有效
        if 'visitor_phone_number' not in data or not data['visitor_phone_number']:
            return {'error': '访客手机号码不能为空'}, 400
        if not validate_phone_number(data['visitor_phone_number']):
            return {'error': '访客手机号码格式有误'}, 400

        # 校验用户是否存在
        if not User.query.filter_by(id_number=data['visitor_id_number'], phone_number=data['visitor_phone_number'], is_deleted=False).first():
            return {'error': '该用户不存在'}, 400

        # 校验访客姓名格式是否正确
        if 'visitor_name' not in data or not data['visitor_name']:
            return {'error': '访客姓名不能为空'}, 400
        if not validate_name(data['visitor_name']):
            return {'error': '访客姓名格式有误'}, 400

        # 校验访客性别是否正确
        if 'visitor_gender' not in data or not data['visitor_gender']:
            return {'error': '访客性别不能为空'}, 400
        if not validate_gender(data['visitor_gender']):
            return {'error': '访客性别格式有误'}, 400

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
        visitor_log.visitor_name = data['visitor_name']
        visitor_log.visitor_gender = data['visitor_gender']
        visitor_log.visitor_phone_number = data['visitor_phone_number']
        visitor_log.visitor_id_type = data['visitor_id_type']
        visitor_log.visitor_id_number = data['visitor_id_number']
        visitor_log.visitor_org = data.get('visitor_org') or ''
        visitor_log.visited_person_name = data.get('visited_person_name') or ''
        visitor_log.visited_person_org = data.get('visited_person_org') or ''
        visitor_log.reason = data.get('reason') or ''
        visitor_log.accompanying_people = data.get('accompanying_people') or ''
        visitor_log.license_plate = data.get('license_plate') or ''

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
            visitor_log.deleted_at = datetime.now()

            # 提交数据库更新
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return {'error': '数据库更新失败: {}'.format(str(e))}, 500
            return {'message': '访客记录删除成功'}, 200

        return {'error': '访客记录未找到'}, 404


    @staticmethod
    def search_visitor_logs(json_string, page=1, per_page=10, sort_field='id', sort_order='asc'):
        """检索访客记录"""

        # 将参数中的json字符串转换成字典
        filters = {}
        if json_string:
            try:
                filters = json.loads(json_string)  # 将字符串转换为字典
            except ValueError:
                return {"error": "无效的 JSON"}, 400

        # 检查 sort_field 是否是 VisitorLog 模型中的有效列
        if sort_field not in VisitorLog.__table__.columns:
            return {'error': '无效的排序字段'}, 400

        # 创建查询对象
        query = VisitorLog.query.filter(VisitorLog.is_deleted==False)

        # 如果有访问时间的条件
        if filters.get('start_time') and filters.get('end_date'):
            query = query.filter(
                VisitorLog.visit_time >= string_to_datetime(filters['start_time']),
                VisitorLog.visit_time < string_to_datetime(filters['end_date'])
            )

        # 如果有访客类型的条件
        if filters.get('visit_type'):
            query = query.filter(VisitorLog.visit_type == filters['visit_type'])

        # 如果有校区名称的条件
        if filters.get('campus'):
            query = query.filter(VisitorLog.campus == filters['campus'])

        # 如果有访客所属单位的条件
        if filters.get('visitor_org'):
            query = query.filter(VisitorLog.visitor_org.contains(filters['visitor_org']))

        # 如果有访客姓名的条件
        if filters.get('visitor_name'):
            query = query.filter(VisitorLog.visitor_name.contains(filters['visitor_name']))

        # 如果有被访人姓名的条件
        if filters.get('visited_person_name'):
            query = query.filter(VisitorLog.visited_person_name.contains(filters['visited_person_name']))

        # 如果有被访人部门的条件
        if filters.get('visited_person_org'):
            query = query.filter(VisitorLog.visited_person_org.contains(filters['visited_person_org']))

        # 如果有车牌号码的条件
        if filters.get('license_plate'):
            query = query.filter(VisitorLog.license_plate.contains(filters['license_plate']))

        # 如果有是否审批通过的条件
        if filters.get('is_approved'):
            query = query.filter(VisitorLog.is_approved == filters['is_approved'])

        # 如果有是否取消的条件
        if filters.get('is_cancelled'):
            query = query.filter(VisitorLog.is_cancelled == filters['is_cancelled'])

        # 动态排序，确保sort_field是数据库表中的有效字段
        if sort_order.lower() == 'asc':
            query = query.order_by(asc(getattr(VisitorLog, sort_field)))
        elif sort_order.lower() == 'desc':
            query = query.order_by(desc(getattr(VisitorLog, sort_field)))
        else:
            # 如果排序顺序无效，则默认使用升序
            query = query.order_by(asc(getattr(VisitorLog, sort_field)))

        # 分页
        paginated_visitor_logs = query.paginate(page=page, per_page=per_page, error_out=False)

        # 返回分页后的数据、总页数、当前页和每页记录数
        return {
            "visitor_logs": [visitor_log.to_dict() for visitor_log in paginated_visitor_logs.items],
            "total_pages": paginated_visitor_logs.pages,
            "current_page": page,
            "per_page": per_page
        }, 200


    @staticmethod
    def approve_visitor_log(user, visitor_log_id, data):
        """审批预约申请"""

        # 查找现有的访客记录
        visitor_log = VisitorLog.query.filter_by(id=visitor_log_id, is_deleted=False).first()
        if not visitor_log:
            return {'error': '访客记录未找到'}, 404

        # 已审批的访客记录无法修改
        if visitor_log.is_approved is not None:
            return {'error': '该访客记录已被审批'}, 400

        # 已取消的访客记录无法修改
        if visitor_log.is_cancelled:
            return {'error': '该访客记录已被取消'}, 400

        # 校验审批标记
        if 'is_approved' not in data:
            return {'error': '审批标记不能为空'}, 400
        if not isinstance(data['is_approved'], bool):
            return {'error': '审批标记格式有误'}, 400

        # 校验审批备注是否为空
        if 'approval_note' not in data or not data['approval_note'] or len(data['approval_note']) < 2:
            return {'error': '审批备注不能为空且至少为2个字符'}, 400


        visitor_log.is_approved = data['is_approved']
        visitor_log.approval_note = data['approval_note']
        visitor_log.approver = user.name
        visitor_log.approved_at = datetime.now()

        # 提交数据库更新
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': '数据库更新失败: {}'.format(str(e))}, 500
        return visitor_log.to_dict(), 200


    @staticmethod
    def verify_visitor_log(user, visitor_log_id):
        """来访登记"""

        # 查询访客记录
        visitor_log = VisitorLog.query.filter_by(id=visitor_log_id, is_deleted=False).first()

        if not visitor_log:
            return {'error': '访客记录未找到'}, 404

        if visitor_log.is_approved is not True:
            return {'error': '该访客记录尚未审批通过'}, 400

        if is_time_after_now(datetime_to_string(visitor_log.visit_time)):
            return {'error': '当前未到预约时间'}

        if is_time_before_now(datetime_to_string(visitor_log.leave_time)):
            return {'error': '当前已过预约时间'}

        visitor_log.entry_time = datetime.now()
        visitor_log.verifier = user.name

        # 提交数据库更新
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': '数据库更新失败: {}'.format(str(e))}, 500
        return visitor_log.to_dict(), 200