import unittest

import requests
from ddt import ddt, data, unpack
from common.SendRequests import SendRequests
from common.ReadMysql import get_all_sql_data
import os
import sys
from common.BeautifulReport.BeautifulReport import BeautifulReport
from json.decoder import JSONDecodeError

testData = get_all_sql_data()


@ddt
class Test1(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.s = requests.session()

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @data(*testData)
    def test_api(self, data):
        # 将报告展示修改为用例的名字
        self._testMethodName = data['case_name']
        # 将报告展示修改为用例的描述
        self._testMethodDoc = data['case_name']
        if not data['isrun']:
            self.skipTest('teardown case')
        r = SendRequests(testData)
        re = r.sendRequests(self.s, data)
        try:
            res = re.json()
        except JSONDecodeError:
            res = re.content.decode('utf-8')
        print(res)
        for each_result in data["expect_result"].split(','):
            try:
                # 切割字符串去掉空格
                expect_result_key, expect_result_value = each_result.split(":")
                expect_result_key = expect_result_key.strip()
                expect_result_value = expect_result_value.strip()
                # 处理数值类型的返回值
                if 'int(' in expect_result_value:
                    expect_result_value = int(expect_result_value.split('int(')[-1].replace(')', ''))
                # 处理布尔类型的返回值
                if 'bool(' in expect_result_value:
                    expect_result_value = bool(expect_result_value.split('int(')[-1].replace(')', ''))

                # 转换为字符串
                # expect_result = eval(expect_result1)

                self.assertEqual(res[expect_result_key], expect_result_value, "返回错误,实际结果是%s" % res[expect_result_key])
            except ValueError:
                self.assertIn(each_result, str(res), "返回错误,实际结果是%s" % res)

if __name__ == '__main__':
    unittest.main()
