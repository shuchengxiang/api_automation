from ReadExcel import ReadExcel
import requests
import json
import os
from common.util import get_variable_param, get_dependent_param, get_case_by_id


class SendRequests:
    def __init__(self, Datalist):
        self.session = None
        self.isrun = None
        self.method = None
        self.url = None
        self.h = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept - Encoding': 'gzip, deflate, br',
            'Accept - Language': 'zh - CN, zh;q = 0.9',
            'User - Agent': 'Mozilla / 5.0(Windows NT 6.1; WOW64) AppleWebKit / 537.36(KHTML, like Gecko) '
                            'Chrome / 84.0.4147.105 Safari / 537.36'
        }
        self.par = None
        self.v = None
        self.body = None
        self.depending_case = None
        self.teardown_case = None
        self.timeout = 5
        self.Datalist = Datalist
        self.depending_teardowncase = None
        self.depending_res_list = None

    def sendRequests(self, session, apiData):
        """用于发送请求和逻辑处理的请求方法"""
        # 从读取的字典中获取响应的参数作为传递,包括对关键字参数的处理
        str_after_consult = self.get_all_params(apiData)
        if self.depending_case:
            depending_case_list = self.depending_case.split(',')
            if '${' in str_after_consult:
                # 这里需要创建新的实例来运行
                res = SendRequests(self.Datalist).send_depending_requests(session, depending_case_list)
                self.depending_res_list = res
                str_after_consult = get_dependent_param(str_after_consult, '${', res[-1])
            else:
                res = SendRequests(self.Datalist).send_depending_requests(session, depending_case_list)
                self.depending_res_list = res
        self.par = eval(str_after_consult)
        # 发送请求
        re = session.request(method=self.method, url=self.url, headers=self.h, params=self.par,
                                      data=self.body, verify=self.v, timeout=self.timeout)
        # 对case产生的数据进行清理
        if self.teardown_case:
            teardown_case = get_case_by_id(self.Datalist, self.teardown_case)
            SendRequests(self.Datalist).send_teardown_requests(session, teardown_case, re.content.decode('utf-8'))
        # 对case的依赖case产生的数据进行清理
        if self.depending_teardowncase:
            depending_teardowncase_list = self.depending_teardowncase.split(',')
            for i in range(len(depending_teardowncase_list)):
                if depending_teardowncase_list[i] == 'n':
                    continue
                depending_teardowncase = get_case_by_id(self.Datalist, depending_teardowncase_list[i])
                depending_res = self.depending_res_list[i]
                SendRequests(self.Datalist).send_teardown_requests(session, depending_teardowncase, depending_res)
        return re

    def send_depending_requests(self, session, depending_case_list):
        """用于获取依赖数据的请求方法"""
        depending_case_res_list = []
        depending_case_res = None
        for each in depending_case_list:
            apiData = get_case_by_id(self.Datalist, each)
            # 从读取的字典中获取响应的参数作为传递,包括对关键字参数的处理
            str_after_consult = self.get_all_params(apiData)
            # 对依赖参数进行处理
            if '${' in str_after_consult:
                str_after_consult = get_dependent_param(str_after_consult, '${',
                                                        depending_case_res.content.decode('utf-8'))

            self.par = eval(str_after_consult)
            depending_case_res = session.request(method=self.method, url=self.url, headers=self.h,
                                                 params=self.par,
                                                 data=self.body, verify=self.v, timeout=self.timeout)
            res = depending_case_res.content.decode('utf-8')
            depending_case_res_list.append(res)

        return depending_case_res_list

    def send_teardown_requests(self, session, apiData, teardown_res):
        """用于数据清理的请求方法"""
        # 从读取的字典中获取响应的参数作为传递,包括对关键字参数的处理
        str_after_consult = self.get_all_params(apiData)
        # 处理teardowncase包含依赖参数的情况
        if '${' in str_after_consult:
            str_after_consult = get_dependent_param(str_after_consult, '${', teardown_res)
        self.par = eval(str_after_consult)
        # 发送请求
        re = session.request(method=self.method, url=self.url, headers=self.h, params=self.par,
                                  data=self.body, verify=self.v, timeout=self.timeout)
        return re

    def get_all_params(self, apiData):
        self.method = apiData["method"]
        self.url = apiData["url"]
        self.depending_case = apiData['depending_case']
        self.teardown_case = apiData['teardown_case']
        self.depending_teardowncase = apiData['depending_teardowncase']
        self.isrun = apiData['isrun']
        if apiData["headers"]:
            self.h = eval(apiData["headers"])
        str_after_consult = ''
        # 对参数的处理
        if apiData["params"]:
            str_after_consult = apiData["params"]
            # 处理md5加密参数转换
            if 'md5(' in str_after_consult:
                str_after_consult = get_variable_param(str_after_consult, 'md5(')

            if 'timestamp(' in str_after_consult:
                str_after_consult = get_variable_param(str_after_consult, 'timestamp(')
        return str_after_consult




if __name__ == '__main__':
    s = requests.session()
    path = os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data"), "apiTest.xlsx")
    testData = ReadExcel(path, "Sheet1").get_all_data()
    response = SendRequests(testData).sendRequests(s, testData[0])
    print(response)
