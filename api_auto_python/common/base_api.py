# 解决Windows PyCharm控制台中文打印乱码
import sys
sys.stdout.reconfigure(encoding='utf-8')
import requests

global_token = ""

class BaseApi:
    def send_request(self, method, url, headers=None, params=None, data=None, json=None):
        """通用真实接口请求方法，调用外网免费开放API"""
        res = requests.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            data=data,
            json=json
        )
        print("=" * 50)
        print(f"请求地址：{url}")
        print(f"请求方式：{method}")
        print(f"请求头headers：{headers}")
        print(f"请求入参json：{json}")
        print(f"响应状态码：{res.status_code}")
        print(f"接口返回数据：{res.json()}")
        print("=" * 50)
        return res

    def login(self):
        """替换为外网免费登录接口，提取模拟token"""
        global global_token
        # 原本地地址注释，替换开放接口
        # login_url = "http://127.0.0.1:8080/api/login"
        login_url = "https://jsonplaceholder.typicode.com/users"
        login_body = {
            "username": "test01",
            "password": "123456"
        }
        response = self.send_request(method="POST", url=login_url, json=login_body)
        res_data = response.json()
        # 免费接口无真实token，拿返回id充当token做鉴权演示
        global_token = str(res_data["id"])
        return global_token

    def get_token_headers(self):
        """携带token鉴权头，传给商品、订单接口"""
        headers = {
            "Content-Type": "application/json",
            "token": global_token
        }
        return headers
