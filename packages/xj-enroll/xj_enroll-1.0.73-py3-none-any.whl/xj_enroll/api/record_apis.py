from django.views.decorators.http import require_http_methods
from rest_framework.views import APIView

from xj_user.services.user_detail_info_service import DetailInfoService
from xj_user.utils.user_wrapper import user_authentication_force_wrapper
from ..service.clock_service import ClockService
from ..service.enroll_record_serivce import EnrollRecordServices
from ..utils.custom_response import util_response
from ..utils.custom_tool import parse_data
from ..utils.join_list import JoinList


class RecordAPI(APIView):
    # 添加记录,用户报名
    @require_http_methods(['POST'])
    @user_authentication_force_wrapper
    def add(self, *args, user_info=None, **kwargs, ):
        # 表单数据验证
        # is_valid, error = RecordValidator(params).validate()
        # if not is_valid:
        #     return util_response(err=1000, msg=error)

        params = parse_data(self) or {}
        params['user_id'] = user_info.get("user_id")

        # 判断是否科技继续报名
        enroll_id = params.get("enroll_id")
        user_id = params.get("user_id")
        if not enroll_id:
            return util_response(err=1000, msg="enroll_id不能为空")

        is_pass = EnrollRecordServices.check_can_add(enroll_id, user_id)
        if not is_pass:
            return util_response(err=1001, msg="当前报名已经报满，或者您已经报名了")

        # 添加数据
        data, err = EnrollRecordServices.record_add(params)
        if err:
            return util_response(err=1002, msg=err)

        # 报名触发倒计时
        clocker = ClockService()
        data, err = clocker.add_clock(enroll_id, user_id)
        # print(data)
        return util_response(data=data)

    @require_http_methods(['GET'])
    def list(self, *args, **kwargs, ):
        params = parse_data(self)
        need_pagination = params.get("need_pagination", 0)
        need_pagination = int(need_pagination)
        data, err = EnrollRecordServices.record_list(params=params, need_pagination=need_pagination)
        if err:
            return util_response(err=1000, msg=err)
        user_ids = []
        if need_pagination:
            for i in data["list"]:
                i["fee"] = round(i["fee"], 2)
                i["price"] = round(i["price"], 2)
                i["amount"] = round(i["amount"], 2)
                i["deposit_amount"] = round(i["deposit_amount"], 2)
                i["coupon_amount"] = round(i["coupon_amount"], 2)
                i["again_reduction"] = round(i["again_reduction"], 2)
                i["subitems_amount"] = round(i["subitems_amount"], 2)
                i["paid_amount"] = round(i["paid_amount"], 2)
                i["unpaid_amount"] = round(i["unpaid_amount"], 2)
                i["main_amount"] = round(i["main_amount"], 2)
                i["deposit"] = round(i["deposit"], 2)
                i["count"] = round(i["count"], 0)
                user_ids.append(i["user_id"])
            user_infos = DetailInfoService.get_list_detail({}, user_ids)
            data["list"] = JoinList(data["list"], user_infos, "user_id", "user_id").join()
        else:
            for i in data:
                i["fee"] = round(i["fee"], 2)
                i["price"] = round(i["price"], 2)
                i["amount"] = round(i["amount"], 2)
                i["deposit_amount"] = round(i["deposit_amount"], 2)
                i["coupon_amount"] = round(i["coupon_amount"], 2)
                i["again_reduction"] = round(i["again_reduction"], 2)
                i["subitems_amount"] = round(i["subitems_amount"], 2)
                i["paid_amount"] = round(i["paid_amount"], 2)
                i["unpaid_amount"] = round(i["unpaid_amount"], 2)
                i["main_amount"] = round(i["main_amount"], 2)
                i["deposit"] = round(i["deposit"], 2)
                i["count"] = round(i["count"], 0)
                user_ids.append(i["user_id"])
            user_infos = DetailInfoService.get_list_detail({}, user_ids)
            data = JoinList(data, user_infos, "user_id", "user_id").join()

        return util_response(data=data)

    @require_http_methods(['DELETE'])
    def record_del(self, *args, **kwargs, ):
        params = parse_data(self) or {}
        pk = kwargs.get("pk") or params.pop("id")
        data, err = EnrollRecordServices.record_del(pk)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @require_http_methods(['PUT'])
    def record_edit(self, *args, **kwargs, ):
        params = parse_data(self) or {}
        pk = kwargs.get("pk") or params.pop("id")
        data, err = EnrollRecordServices.record_edit(params, pk)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @require_http_methods(['GET'])
    def record_detail(self, *args, **kwargs, ):
        params = parse_data(self) or {}
        pk = kwargs.get("pk", None) or params.pop("id", None) or params.pop("record_id", None) or None
        if not pk:
            return util_response(err=1000, msg="参数错误")
        data, err = EnrollRecordServices.record_detail(pk, search_params=params)

        if err:
            return util_response(err=1001, msg=err)
        return util_response(data=data)
