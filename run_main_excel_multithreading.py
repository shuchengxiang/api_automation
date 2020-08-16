from common.ReadExcel import ReadExcel
import os
from common.RunTestCase import run_test_case
from common.BeautifulReport.BeautifulReport import BeautifulReport, FIELDS_T
import time
from tomorrow import threads

path = os.path.join(os.path.join(os.path.dirname(__file__), "excel_data"), "apiTest.xlsx")
testData = ReadExcel(path, "Sheet1").get_all_data()

if __name__ == '__main__':
    current_time = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    # 生成测试报告的路径
    log_path = os.path.join(os.path.dirname(__file__), "report")
    test_set = run_test_case(testData, testData)
    # BeautifulReport(test_set).report(filename='测试报告' + current_time, description=u'东奥商城',
    #                                        log_path=log_path)
    global FIELDS_T
    FIELDS_T = {
        "testPass": 0,
        "testResult": [
        ],
        "testName": "",
        "testAll": 0,
        "testFail": 0,
        "beginTime": "",
        "totalTime": "",
        "testError": 0,
        "testSkip": 0
    }

    @threads(10)
    def run_case_b(test_set):
        BeautifulReport(test_set).report(filename='测试报告' + current_time, description=u'东奥商城',
                                           log_path=log_path, multithread=True)
    for each in test_set:
        run_case_b(each)
