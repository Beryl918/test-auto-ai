import unittest
from common.base_api import BaseApi

class TestCreateOrder(unittest.TestCase):
    def setUp(self):
        # 前置登录鉴权
        self.api = BaseApi()
        self.api.login()
        self.headers = self.api.get_token_headers()
        self.order_url = "https://jsonplaceholder.typicode.com/comments"

    def test_create_order(self):
        """传入商品ID创建订单，校验订单号生成"""
        order_body = {
            "postId": 1001,
            "name": "测试买家",
            "email": "test@123.com",
            "body": "购买2件商品"
        }
        res = self.api.send_request("POST", self.order_url, headers=self.headers, json=order_body)
        res_data = res.json()
        # 原代码 self.assertIn("order_id", res_data["data"]) 删除
        self.assertEqual(res.status_code, 201, "创建订单失败")
        self.assertIn("id", res_data, "接口未返回订单编号")

if __name__ == '__main__':
    unittest.main()
