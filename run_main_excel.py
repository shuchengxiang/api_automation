from common.ReadExcel import ReadExcel
import os
from common.RunTestCase import run_test_case
from common.BeautifulReport.BeautifulReport import BeautifulReport
import time

path = os.path.join(os.path.join(os.path.dirname(__file__), "excel_data"), "apiTest.xlsx")
testData = ReadExcel(path, "Sheet1").get_all_data()

if __name__ == '__main__':
    current_time = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    # 生成测试报告的路径
    log_path = os.path.join(os.path.dirname(__file__), "report")
    test_set = run_test_case(testData, testData)
    BeautifulReport(test_set).report(filename='测试报告' + current_time, description=u'东奥商城',
                                           log_path=log_path)

