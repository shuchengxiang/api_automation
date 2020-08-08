import unittest
import time
import os
from common.HTMLTestRunner import HTMLTestRunner
from common.BeautifulReport.BeautifulReport import BeautifulReport


def run_case(dir="testcase"):
    case_dir = os.path.join(os.path.abspath(os.getcwd()), dir)
    # test_case = unittest.TestSuite()
    discover = unittest.defaultTestLoader.discover(case_dir, pattern="test_case_sql_01.py", top_level_dir=None)
    return discover


def run_main_sql():
    current_time = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    # 生成测试报告的路径
    log_path = os.path.join(os.path.dirname(__file__), "report")
    BeautifulReport(run_case()).report(filename='测试报告' + current_time, description=u'东奥商城',
                                       log_path=log_path)


if __name__ == '__main__':
    run_main_sql()
