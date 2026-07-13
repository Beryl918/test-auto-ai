import sys
import os
# 兼容导包路径
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_path not in sys.path:
    sys.path.append(root_path)

import unittest
from common.base_api import BaseApi

class TestGoodsList(unittest.TestCase):
    def setUp(self):
        self.api = BaseApi()
        self.api.login()
        self.headers = self.api.get_token_headers()
        # 开放商品接口地址
        self.goods_url = "https://jsonplaceholder.typicode.com/posts"

    def test_query_goods(self):
        """携带token查询商品列表，分页GET请求"""
        query_params = {"_page": 1, "_limit": 10}
        res = self.api.send_request("GET", self.goods_url, headers=self.headers, params=query_params)
        res_data = res.json()

        # ========== 修改后的断言（适配开放接口） ==========
        # 1. 校验接口状态码200
        self.assertEqual(res.status_code, 200, "商品查询接口返回失败")
        # 2. 校验返回数据是列表
        self.assertIsInstance(res_data, list, "商品列表数据格式错误")
        # 3. 校验列表有数据（不为空）
        self.assertGreater(len(res_data), 0, "商品列表为空")
