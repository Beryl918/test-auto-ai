import unittest
# 导入全部测试用例类
from test_case.test_login import TestLoginApi
from test_case.test_goods import TestGoodsList
from test_case.test_order import TestCreateOrder

# 构建测试套件
suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestLoginApi))
suite.addTest(unittest.makeSuite(TestGoodsList))
suite.addTest(unittest.makeSuite(TestCreateOrder))

# 执行并打印详细测试结果
if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
