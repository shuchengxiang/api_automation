import hashlib
import time


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
        # 在依赖参数的返回中取值
        response_value_start_index = str_response.index(value_in_response) + len(value) + 3
        response_value = str_response[response_value_start_index: str_response.index(',', response_value_start_index)]
        str1 = str1.replace(f'{tag}{value}'+'}', response_value)
    return str1


def get_case_by_id(datalist, id):
    for data in datalist:
        if int(data['id']) == int(id):
            return data
    return '没有找到该case'