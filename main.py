# -*- coding: UTF-8 -*-
"""
@Project ：Taobaoke_Api 
@File    ：main.py
@IDE     ：PyCharm 
@Author  ：胖妞
@Date    ：2022/1/16 16:04
"""

import random
from fastapi import FastAPI
import uvicorn

from pdd_sdk import PddApiClient, getRecommendGoods, promotionForGoods, genUrlForGoods

app = FastAPI()
pid = '31409226_235210625'  # 推广位id
pdd = PddApiClient(app_key='7c5c1386ab944ac5921113721aa5d1f6',
                   secret_key='7236dac66ee9173cc2da9113f6cc9c067848292a')


@app.get('/')
def index():
    return 'Pdd Api Started!'


# 获取热榜商品
@app.get('/pdd/recommend')
def recommend():
    recommend_goods = getRecommendGoods(pdd, pid)
    search_id = recommend_goods['goods_basic_detail_response']['search_id']  # 搜索id，建议生成推广链接时候填写，提高收益。
    # 随机抽取一条优惠
    goods_list = recommend_goods['goods_basic_detail_response']['list']
    random_goods = random.choice(goods_list)
    # 生成推广链接
    promotion_goods_info = promotionForGoods(pdd, pid, random_goods['goods_sign'], search_id)
    # 拆解商品信息
    goods_name = random_goods['goods_name']
    goods_thumbnail_url = random_goods['goods_thumbnail_url']
    min_group_price = random_goods['min_group_price']
    coupon_discount = random_goods['coupon_discount']
    goods_info = {
        'msg': '随机获取推广商品成功',
        'data': {
            'goods_name': goods_name,
            'goods_thumbnail_url': goods_thumbnail_url,
            'price': float(min_group_price / 100),
            'discount_price': float((min_group_price - coupon_discount) / 100),
            'url': promotion_goods_info['goods_promotion_url_generate_response']['goods_promotion_url_list'][0][
                'we_app_web_view_short_url']
        }
    }
    return goods_info


# 商品转链
@app.get('/pdd/gen')
def gen(url: str):
    return {'msg': '随机获取推广商品成功', 'data': genUrlForGoods(pdd, pid, url)}


if __name__ == '__main__':
    uvicorn.run(app='main:app', host="127.0.0.1", port=7890, reload=True, debug=True)
