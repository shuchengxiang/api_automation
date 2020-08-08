from flask import Flask
from database_data.case_model import Case, db
from app import app

query_result = Case.query.all()


def get_sql_data(result):
    apiData = []
    for each in result:
        dict_result = {}
        for c in each.__table__.columns:
            dict_result[c.name] = str(getattr(each, c.name))
        apiData.append(dict_result)
    return apiData


if __name__ == '__main__':
    apiData = get_sql_data(query_result)
    print(apiData)

    # a = Case.query.all()
    # print(a)











