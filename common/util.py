import hashlib
import time
import unittest


def indexstr(str1, str2):
    """查找指定字符串str1包含指定子字符串str2的全部位置，以列表形式返回"""
    lenth2 = len(str2)
    lenth1 = len(str1)
    indexstr2 = []
    i = 0
    while str2 in str1[i:]:
        indextmp = str1.index(str2, i, lenth1)
        indexstr2.append(indextmp)
        i = (indextmp + lenth2)
    return indexstr2


def get_variable_param(str1, tag):
    """根据标志替换参数，返回替换后的值"""
    location_list = indexstr(str1, tag)
    for i in location_list:
        value = str1[i: str1.index(')', i)].replace(tag, '')
        value_result = ''
        if tag == 'md5(':
            value_result = '\'' + hashlib.md5(value.encode('utf-8')).hexdigest() + '\''
        if tag == 'timestamp(':
            value_result = str(time.time() * 1000)[0:int(value)]
        str1 = str1.replace(f'{tag}{value})', value_result)
    return str1


def get_dependent_param(str1, tag, str_response):
    """根据标志从字符串中获取标志内的参数并返回替换为依赖参数的整个字符串"""
    location_list = indexstr(str1, tag)
    for i in location_list:
        # 在本请求的参数中取值
        value = str1[i: str1.index('}', i)].replace(tag, '')
        value_in_response = '\"' + value + '\"'
        if value_in_response in str_response:
            pass
        else:
            value_in_response = '\'' + value + '\''
        try:
            # 在依赖参数的返回中取值
            response_value_start_index = str_response.index(value_in_response) + len(value) + 3
        except ValueError as e:
            print('依赖接口返回', str_response)
            print('需要的参数为', value_in_response)
            raise ValueError(e)
        response_value = str_response[response_value_start_index: str_response.index(',', response_value_start_index)]
        str1 = str1.replace(f'{tag}{value}'+'}', response_value)
    return str1


def get_case_by_id(datalist, id):
    for data in datalist:
        if int(data['id']) == int(id):
            return data
    return '没有找到该case'


def get_final_case_data(testData, allData):
    """处理优先执行的case，将它们放在data列表的最前面"""
    run_first_list = []
    for each in allData:
        if each['run_first'] == '是':
            run_first_list.append(each)
            if each in testData:
                testData.remove(each)
    run_first_list.extend(testData)
    final_testData = run_first_list
    return final_testData


def assert_method(str1, res):
    try:
        # 切割字符串去掉空格
        expect_result_key, expect_result_value = str1.split(":")
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
        unittest.TestCase().assertEqual(res[expect_result_key], expect_result_value, "返回错误,实际结果是%s" % res[expect_result_key])
    except ValueError:
        unittest.TestCase().assertIn(str1, str(res), "返回错误,实际结果是%s" % res)
