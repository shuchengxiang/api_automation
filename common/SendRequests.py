from ReadExcel import ReadExcel
import requests
import json
import os


class SendRequests:
    def __init__(self, apiData):
        # 从读取的表格中获取响应的参数作为传递
        self.method = apiData["method"]
        self.url = apiData["url"]
        if apiData["params"] == "":
            self.par = None
        else:
            self.par = eval(apiData["params"])

        if apiData["headers"] == "":
            self.h = None
        else:
            self.h = eval(apiData["headers"])

        if apiData["body"] == "":
            self.body_data = None
        else:
            self.body_data = eval(apiData["body"])

        self.ytype = apiData["ytype"]
        self.v = False
        if self.ytype == "json":
            self.body = json.dumps(self.body_data)
        if self.ytype == "data":
            self.body = self.body_data
        else:
            self.body = self.body_data

    def sendRequests(self, s):
        # 发送请求
        re = s.request(method=self.method, url=self.url, headers=self.h, params=self.par, data=self.body, verify=self.v,
                       timeout=5)
        return re

if __name__ == '__main__':
    s = requests.session()
    path = os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data"), "apiTest.xlsx")
    testData = ReadExcel.readExcel(path, "Sheet1")
    response = SendRequests(testData[0]).sendRequests(s)
    print(response)
