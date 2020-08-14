import unittest
import requests
from ddt import ddt, data, unpack
from common.SendRequests import SendRequests
from json.decoder import JSONDecodeError
from util import assert_method


def run_test_case(testData, allData):
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
            if data['isrun'] == '否':
                self.skipTest('teardown case')
            r = SendRequests(allData)
            re = r.send_requests(self.s, data)
            try:
                res = re.json()
            except JSONDecodeError:
                res = re.content.decode('utf-8')
            # 输出时对<script>标签进行处理，防止报告跑版
            print(str(res).replace('<script', '<script1').replace('</script>', '</script1>'))
            for each_result in data["expect_result"].split(','):
                assert_method(each_result, res)

    s = unittest.TestLoader().loadTestsFromTestCase(TestCaseSet)
    return s