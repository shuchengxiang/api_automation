import os
from common.RunTestCase import run_test_case
from common.BeautifulReport.BeautifulReport import BeautifulReport
import time
from database_data.case_model import get_all_sql_data, get_sql_data
from app import app
import unittest
from common.util import get_final_case_data


allData = get_all_sql_data()
testData = get_sql_data([5])
testData = get_final_case_data(testData, allData)

if __name__ == '__main__':
    current_time = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    # 生成测试报告的路径
    log_path = os.path.join(os.path.dirname(__file__), "report")
    # BeautifulReport(run_test_case(testData, allData)).report(filename='测试报告' + current_time, description=u'东奥商城',
    #                                    log_path=log_path)
    unittest.TextTestRunner().run(run_test_case(testData, allData))
