# encoding: utf-8
"""
@project: djangoModel->user_info_service
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 用户信息服务
@created_time: 2022/6/27 19:51
"""

from django.db.models import F

from ..models import ExtendField, DetailInfo, BaseInfo
from ..utils.model_handle import *


class DetailInfoService:
    @staticmethod
    def transform_params(request_dict):
        if not request_dict:
            return {}
        # 冗余字段 请求参数转换
        filed_map = ExtendField.objects.values()
        filed_map = {item['field']: item['field_index'] for item in filed_map}
        return {filed_map.get(k, k): v for k, v in request_dict.items()}

    @staticmethod
    def transform_result(result):
        # 冗余字段 结果集转换
        filed_map = list(ExtendField.objects.all().values("field", 'field_index'))
        filed_map = {item['field_index']: item['field'] for item in filed_map}
        transformed_list = []
        if type(result) is dict:
            result = [result]
        for item in result:
            transformed_dict = {}
            for k, v in item.items():
                if k in filed_map.keys():
                    transformed_dict[filed_map[k]] = v
                    continue
                elif k[0:5] == "field":
                    continue
                else:
                    transformed_dict[k] = v
            transformed_list.append(transformed_dict)
        return transformed_list

    @staticmethod
    def get_list_detail(params, user_id_list=None):
        if not user_id_list is None:
            res_obj = DetailInfo.objects.filter(user_id__in=user_id_list) \
                .annotate(full_name=F("user__full_name")) \
                .annotate(user_name=F("user__user_name")) \
                .annotate(nickname=F("user__nickname"))

            res_data = []
            if res_obj:
                res_data = res_obj.values("user_id", "user_name", "nickname", "full_name", "avatar")
            return res_data

        # 查询用户详细信息列表
        transformed_dict = DetailInfoService.transform_params(params)
        page = transformed_dict.pop('page', 1)
        limit = transformed_dict.pop('limit', 20)
        try:
            list_set = DetailInfo.objects.filter(**transformed_dict)
            count = DetailInfo.objects.filter(**transformed_dict).count()
        except Exception as e:
            return util_response("", 7557, status.HTTP_400_BAD_REQUEST, e.__str__())
        # 分页数据
        page_set = list(Paginator(list_set.values(), limit).page(page))
        final_res_dict = DetailInfoService.transform_result(page_set)
        # 数据拼装
        result = {'list': final_res_dict, 'limit': int(limit), 'page': int(page), 'count': count}
        return result, None

    @staticmethod
    def get_detail(user_id):
        user_base = BaseInfo.objects.filter(id=user_id).first()
        if not user_base:
            return None, '用户不存在'

        user_detail = DetailInfo.objects.filter(user_id=user_id) \
            .annotate(user_name=F("user_id__user_name")) \
            .annotate(nickname=F("user_id__nickname")) \
            .annotate(phone=F("user__phone")) \
            .annotate(email=F("user__email")) \
            .annotate(register_time=F("user__register_time")) \
            .values().first()

        # 获取扩展字段
        field_set = ExtendField.objects.all().values("field", 'field_index')
        field_dict = {item['field_index']: item['field'] for item in field_set}  # 输出的时候弄返了，修改过来

        # 模型字段
        model_fields = DetailInfo._meta.fields
        model_fields = [model_fields[i].name for i in range(len(model_fields))] + list(field_dict.values())
        model_fields = [i for i in model_fields if not i[0:6] == "field_"]

        if not user_detail:
            user_base_info = user_base.to_json()
            user_base_info_fields = user_base_info.keys()
            for i in model_fields:
                if i in user_base_info_fields:
                    continue
                user_base_info.update({i: ""})
            user_base_info["user_id"] = user_base_info["id"]
            return format_params_handle(
                param_dict=user_base_info,
                alias_dict={"user": "user_id"}
            ), None

        # 获取数据
        alias_dict = format_params_handle(
            param_dict=user_detail,
            alias_dict=field_dict
        )
        alias_dict = {k: v for k, v in alias_dict.items() if not field_dict.get(k, k)[0:6] == "field_"}
        return alias_dict, None

    @staticmethod
    def create_or_update_detail(params):

        user_base = BaseInfo.objects.filter(id=params.get('user_id'))
        if not user_base:
            return None, '用户不存在'

        # 判断是否添加过
        user_obj = DetailInfo.objects.filter(user_id=params.get('user_id'))
        transformed_params = DetailInfoService.transform_params(params)
        try:
            if not user_obj:  # 没有添加，进行添加操作
                DetailInfo.objects.create(**transformed_params)
            else:  # 添加过，进行修改操作
                nickname = transformed_params.pop('nickname', None)
                transformed_params.pop('user_id')
                if nickname:
                    user_base.update(nickname=nickname)
                user_obj.update(**transformed_params)
            return None, None
        except Exception as e:
            return None, "参数配置错误：" + str(e)
