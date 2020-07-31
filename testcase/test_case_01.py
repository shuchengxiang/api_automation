import unittest

import requests
from ddt import ddt, data, unpack
from common.SendRequests import SendRequests
from common.ReadExcel import ReadExcel
import os

path = os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data"), "apiTest.xlsx")
print(path)
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
        print(re.json())

        for each_result in data["expect_result"].split(','):
            # 切割字符串去掉空格
            expect_result_key, expect_result_value = each_result.split(":")
            expect_result_key = expect_result_key.strip()
            expect_result_value = expect_result_value.strip()
            # 处理数值类型的返回值
            if 'int(' in expect_result_value:
                expect_result_value = int(expect_result_value.split('int(')[-1].replace(')', ''))
            # 转换为字符串
            # expect_result = eval(expect_result1)

            self.assertEqual(re.json()[expect_result_key], expect_result_value,
                             "返回错误,实际结果是%s" % re.json()[expect_result_key])

if __name__ == '__main__':
    unittest.main()
