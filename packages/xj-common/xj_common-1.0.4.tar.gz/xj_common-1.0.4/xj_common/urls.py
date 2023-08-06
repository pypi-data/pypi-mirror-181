from django.urls import re_path

from xj_common.api import region_api
from xj_common.api.translate_apis import TranslateApis

urlpatterns = [
    # 地区相关API
    re_path(r'^region_list/?$', region_api.RegionAPIS.region_list, ),
    re_path(r'^region_tree/?$', region_api.RegionAPIS.get_region_tree, ),
    re_path(r'^region_add/?$', region_api.RegionAPIS.region_add, ),
    re_path(r'^region_edit/?$', region_api.RegionAPIS.region_edit, ),
    re_path(r'^region_del/?$', region_api.RegionAPIS.region_del, ),
    # 公共翻译
    re_path(r'^translate_article/?$', TranslateApis.translate_article, ),
    re_path(r'^translate_test/?$', TranslateApis.as_view(), ),
    # 公共定位服务
]
