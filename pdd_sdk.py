# -*- coding: UTF-8 -*-
"""
@Project ：Epic 
@File    ：pdd_sdk.py
@IDE     ：PyCharm 
@Author  ：胖妞
@Date    ：2022/1/16 16:04
"""

import requests
import hashlib
import time
import json

PDD_API_ROOT = 'https://gw-api.pinduoduo.com/api/router'


class PddApiClient(object):
    def __init__(self, app_key, secret_key):
        self.app_key = app_key
        self.secret_key = secret_key

    def get_sign(self, params):
        params_list = sorted(list(params.items()), key=lambda x: x[0])
        params_bytes = (self.secret_key + ''.join("%s%s" % (k, v) for k, v in params_list) + self.secret_key).encode(
            'utf-8')
        sign = hashlib.md5(params_bytes).hexdigest().upper()
        return sign

    def call(self, method, param_json, **kwargs):
        params = {
            "type": method,
            "data_type": "JSON",
            "client_id": self.app_key,
            "timestamp": int(time.time()),
        }
        if isinstance(param_json, (dict, list)):
            for key in param_json:
                params[key] = param_json[key]
        params['sign'] = self.get_sign(params)
        resp = requests.get(PDD_API_ROOT, params=params, **kwargs)
        # print(resp.url)
        return json.loads(resp.text)


# 获取热门推荐商品
def getRecommendGoods(pdd,pid):
    recommend_resp = pdd.call("pdd.ddk.goods.recommend.get", {
        'p_id': pid,
        'limit	': 20,
    })
    return recommend_resp


# 多多进宝推广链接生成
def promotionForGoods(pdd, pid, goods_sign_list, search_id):
    promotion_resp = pdd.call("pdd.ddk.goods.promotion.url.generate", {
        'p_id': pid,
        'goods_sign_list': '["' + goods_sign_list + '"]',
        'search_id': search_id,
        'generate_we_app': 'true',
        'material_id': 'true'
    })
    return promotion_resp


# 商品转链
def genUrlForGoods(pdd,pid, url):
    gen_resp = pdd.call("pdd.ddk.goods.zs.unit.url.gen", {
        'pid': pid,
        'source_url': url
    })
    return gen_resp
