import unittest

import requests
from ddt import ddt, data, unpack
from common.SendRequests import SendRequests
from common.ReadExcel import ReadExcel
import os

path = os.path.join(os.path.join(os.path.abspath(os.getcwd()), "data"), "apiTest.xlsx")
testData = ReadExcel.readExcel(path, "Sheet1")


@ddt
class Test1(unittest.TestCase):

    def setUp(self):
        self.s = requests.session()

    def tearDown(self):
        pass

    @data(*testData)
    def test_qq_api(self, data):
        re = SendRequests(data).sendRequests(self.s)
        print(re.json(), 111)

        # 切割字符串取后面的部分
        expect_result1 = data["expect_result"].split(":")[1]
        # 转换为字符串
        expect_result = eval(expect_result1)

        self.assertEqual(re.json()["reason"], expect_result, "返回错误,实际结果是%s" % re.json()["reason"])


if __name__ == '__main__':
    unittest.main()
