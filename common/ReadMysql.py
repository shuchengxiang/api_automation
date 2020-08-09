from flask import Flask
from database_data.case_model import Case, db
from app import app


def get_all_sql_data():
    query_result = Case.query.all()
    apiData = []
    for each in query_result:
        dict_result = {}
        for c in each.__table__.columns:
            dict_result[c.name] = str(getattr(each, c.name))
        apiData.append(dict_result)
    return apiData


def get_sql_data(id_list):
    query_result = []
    for each_id in id_list:
        query = Case.query.filter_by(id=each_id).all()
        query_result.extend(query)
    apiData = []
    for each in query_result:
        dict_result = {}
        for c in each.__table__.columns:
            dict_result[c.name] = str(getattr(each, c.name))
        apiData.append(dict_result)
    return apiData


if __name__ == '__main__':
    apiData = get_all_sql_data()
    print(apiData)
    a = get_sql_data([1, 2, 3])
    print(a)











