import unittest
import time
import os
from common.HTMLTestRunner import HTMLTestRunner
from common.BeautifulReport.BeautifulReport import BeautifulReport


def run_case(dir="testcase"):
    case_dir = os.path.join(os.path.abspath(os.getcwd()), dir)
    test_case = unittest.TestSuite()
    discover = unittest.defaultTestLoader.discover(case_dir, pattern="test_case_01.py", top_level_dir=None)
    return discover


if __name__ == '__main__':
    current_time = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    # 生成测试报告的路径
    report_path = os.path.join(os.path.join(os.path.dirname(__file__), "report"), str(current_time + '.html'))
    log_path = os.path.join(os.path.dirname(__file__), "report")
    # fp = open(report_path, "wb")
    # runner = HTMLTestRunner(stream=fp, title=u"自动化测试报告", description=u'qq接口', verbosity=2)
    # runner.run(run_case())
    # fp.close()
    BeautifulReport(run_case()).report(filename='测试报告'+current_time, description=u'qq接口',
                                       log_path=log_path)
