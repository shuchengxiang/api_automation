import unittest
import requests
from ddt import ddt, data, unpack
from common.SendRequests import SendRequests
from common.ReadExcel import ReadExcel
import os
from json.decoder import JSONDecodeError
from util import assert_method


def run_test_case(testData):
    @ddt
    class TestCaseSet(unittest.TestCase):

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
            re = r.send_requests(self.s, data)
            try:
                res = re.json()
            except JSONDecodeError:
                res = re.content.decode('utf-8')
            print(res)
            for each_result in data["expect_result"].split(','):
                assert_method(each_result, res)

    s = unittest.TestLoader().loadTestsFromTestCase(TestCaseSet)
    return s