# encoding: utf-8
"""
@project: djangoModel->enroll_record_serivce
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 用户报名记录
@created_time: 2022/9/17 15:45
"""
from django.core.paginator import Paginator

from ..models import EnrollRecord, Enroll, EnrollSubitemRecord
from ..serializers import EnrollRecordListSerializer, EnrollSubitemRecordSerializer
from ..utils.custom_tool import format_params_handle


class EnrollRecordServices:
    @staticmethod
    def check_can_add(enroll_id, user_id):
        enroll_obj = Enroll.objects.filter(id=enroll_id).first()
        if not enroll_obj:
            # 传递的报名ID不正确
            return False
        need_num = enroll_obj.to_json().get("count")

        enroll_record_obj = EnrollRecord.objects.filter(enroll_id=enroll_id).exclude(enroll_status_code=124)
        if need_num <= enroll_record_obj.count():
            # 报名数量达到限制
            return False

        this_user_record_obj = enroll_record_obj.filter(user_id=user_id).first()
        if this_user_record_obj:
            # 当前用户报名过了，不允许报名了
            return False

        return True

    @staticmethod
    def record_add(params):
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=[
                "enroll_id",
                "user_id",
                "enroll_auth_status_id",
                "enroll_pay_status_id",
                "enroll_status_code",
                "create_time",
                "price",
                "deposit",
                "count",
                "main_amount",
                "coupon_amount",
                "again_reduction",
                "subitems_amount",
                "deposit_amount",
                "amount",
                "paid_amount",
                "unpaid_amount",
                "fee",
                "photos",
                "files",
                "score",
                "reply",
                "remark",
            ],
        )
        # print("params", params)
        enroll_id = params.get("enroll_id")
        if not enroll_id:
            return None, "enroll_id不能为空"
        try:
            # instance, is_create = EnrollRecord.objects.get_or_create(user_id=params["user_id"], enroll_id=params["enroll_id"], defaults=params)
            instance = EnrollRecord.objects.create(**params)
        except Exception as e:
            return None, str(e)
        return instance.to_json(), None

    @staticmethod
    def record_list(params, need_pagination=None):
        size = params.pop('size', 10)
        page = params.pop('page', 1)
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=[
                "id",
                "enroll_id",
                "user_id",
                "enroll_auth_status_id",
                "enroll_pay_status_id",
                "enroll_status_code",
                "create_time",
                "price",
                "deposit",
                "count",
                "main_amount",
                "coupon_amount",
                "again_reduction",
                "subitems_amount",
                "deposit_amount",
                "amount",
                "paid_amount",
                "unpaid_amount",
                "fee",
                "photos",
                "files",
                "score",
                "reply",
                "remark",
            ],
        )
        # PS 124状态码任务取消报名，不予显示
        enroll_obj = EnrollRecord.objects.filter(**params).exclude(enroll_status_code=124).values()
        if not need_pagination:
            return list(enroll_obj), None
        count = enroll_obj.count()
        paginator = Paginator(enroll_obj, size)
        enroll_obj = paginator.page(page)
        enroll_list = list(enroll_obj.object_list)
        data = {'total': count, "page": page, "size": size, 'list': enroll_list}
        return data, None

    @staticmethod
    def record_edit(params, pk):
        pk = params.pop("id", None) or pk
        # print("pk", pk)
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=[
                "enroll", "user_id", "enroll_auth_status_id", "enroll_pay_status_id", "enroll_status_code", "create_time", "price", "deposit", "count", "main_amount", "coupon_amount",
                "again_reduction", "subitems_amount", "deposit_amount", "amount", "paid_amount", "unpaid_amount", "fee", "photos", "files", "score", "reply", "remark",
            ],
        )
        record_obj = EnrollRecord.objects.filter(id=pk)
        if not record_obj.first():
            return None, "没有找到id为" + str(pk) + "的记录"
        try:
            record_obj.update(**params)
        except Exception as e:
            return None, "修改异常:" + str(e)
        return None, None

    @staticmethod
    def record_del(pk, search_params=None):
        if pk:
            record_obj = EnrollRecord.objects.filter(id=pk)
        elif search_params and isinstance(search_params, dict):
            record_obj = EnrollRecord.objects.filter(**search_params)
        else:
            return None, "找不到要删除的数据"

        if not record_obj:
            return None, None
        try:
            record_obj.delete()
        except Exception as e:
            return None, "删除异常:" + str(e)
        return None, None

    @staticmethod
    def record_detail(pk, search_params=None):
        if search_params is None:
            search_params = {}
        if search_params:
            main_record_detail = EnrollRecord.objects.filter(**search_params).first()
        else:
            main_record_detail = EnrollRecordListSerializer(EnrollRecord.objects.filter(id=pk).first(), many=False).data
            subitems_record_list = EnrollSubitemRecordSerializer(EnrollSubitemRecord.objects.filter(enroll_record_id=pk), many=True).data
            main_record_detail["subitem_record_list"] = subitems_record_list

        return main_record_detail, None
