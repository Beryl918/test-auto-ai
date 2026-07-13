import unittest
from common.base_api import BaseApi

class TestLoginApi(unittest.TestCase):
    def setUp(self):
        # 每条用例执行前初始化接口对象
        self.api = BaseApi()

    def test_login_success(self):
        """测试登录成功流程，校验token正常返回"""
        token = self.api.login()
        # 断言：token不为空、长度合法
        self.assertIsNotNone(token, "登录失败，未获取token")
        self.assertTrue(len(token) > 10, "token格式异常")

if __name__ == '__main__':
    unittest.main()
