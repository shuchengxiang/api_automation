from flask import flash, Flask, send_file, url_for, redirect, request
from gettext import gettext
from flask_admin import Admin, expose, expose_plugview
from flask_admin.actions import action
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask_sqlalchemy import SQLAlchemy
from common.RunTestCase import run_test_case
import os
import time
from common.BeautifulReport.BeautifulReport import BeautifulReport
from flask_admin.model.template import EndpointLinkRowAction

db = SQLAlchemy()
# db = SQLAlchemy(app)


class Case(db.Model):
    __tablename__ = 'apitest_case'

    id = db.Column(db.Integer, primary_key=True)
    case_name = db.Column(db.String(1024), unique=False, nullable=False)
    method = db.Column(db.String(1024), unique=False, nullable=False)
    url = db.Column(db.String(1024), unique=False, nullable=False)
    depending_case = db.Column(db.String(1024), unique=False, nullable=True)
    isrun = db.Column(db.String(1024), unique=False, nullable=False, default='是')
    params = db.Column(db.String(4096), unique=False, nullable=False)
    headers = db.Column(db.String(4096), unique=False, nullable=True)
    depending_teardowncase = db.Column(db.String(1024), unique=False, nullable=True)
    teardown_case = db.Column(db.String(1024), unique=False, nullable=True)
    status_code = db.Column(db.String(1024), unique=False, nullable=True)
    expect_result = db.Column(db.String(1024), unique=False, nullable=False)
    msg = db.Column(db.String(1024), unique=False, nullable=True)

    def import_case(self):
        print("import")
        return True


class CaseView(ModelView):
    # 指定模板
    list_template = 'AdminLTE/list.html'
    create_template = 'AdminLTE/create.html'
    edit_template = 'AdminLTE/edit.html'
    details_template = 'AdminLTE/details.html'

    column_display_pk = True
    column_labels = {
        'id': 'ID',
        'case_name': '用例名称',
        'isrun': '是否运行'
    }
    column_searchable_list = ['case_name', 'isrun']
    column_filters = ['case_name', 'isrun']
    can_view_details = True
    can_export = True
    export_types = ['csv', 'xls', 'json', 'html']
    can_set_page_size = True
    show_run_all_button = True

    form_choices = {
        'isrun': [
            ('是', '是'),
            ('否', '否'),
        ]
    }

    # @action('import', '导入', '是否导入数据？')
    # def action_import(self, ids):
    #     try:
    #         count = 0
    #         query = Case.query.filter(Case.id.in_(ids))
    #         for s in query.all():
    #             result = s.import_case()
    #             if not result:
    #                 raise Exception('Empty data')
    #             else:
    #                 count += 1
    #         flash('数据源成功导入！')
    #     except Exception as ex:
    #         if not self.handle_view_exception(ex):
    #             raise
    #         flash(gettext('Failed to import slices. %s' % str(ex)), 'error')

    @action('case_run', '运行用例', '是否运行用例?')
    def case_run(self, ids):
        testData = get_sql_data(ids)
        allData = get_all_sql_data()
        current_time = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
        log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "report")
        BeautifulReport(run_test_case(testData, allData)).report(filename='测试报告' + current_time, description=u'东奥商城',
                                                        log_path=log_path)
        report_filename = os.path.join(log_path, '测试报告' + current_time + '.html')
        return redirect(url_for('.report', path=report_filename))

    @expose('/run_all_case', methods=['POST', 'GET'])
    def run_all_case(self):
        testData = get_all_sql_data()
        allData = testData
        current_time = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
        log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "report")
        BeautifulReport(run_test_case(testData, allData)).report(filename='测试报告' + current_time, description=u'东奥商城',
                                                                 log_path=log_path)
        report_filename = os.path.join(log_path, '测试报告' + current_time + '.html')
        return redirect(url_for('.report', path=report_filename))

    @expose('/report', methods=['POST', 'GET'])
    def report(self):
        path = request.args.get('path')
        filelist = sorted(os.listdir(os.path.dirname(path)))
        # 报告数超过三个则从头删除
        if len(filelist) >= 10:
            os.chdir(os.path.dirname(path))
            os.remove(filelist[0])
        return send_file(path)


admin = Admin(url='/', name='自动化平台', template_mode='bootstrap3', base_template='AdminLTE/mylayout.html', )  # 指定模板
admin.add_view(CaseView(Case, db.session, name='用例管理', menu_icon_type='fa', menu_icon_value='fa-table'))
# admin.add_link(MenuLink(name='模型图谱', url='#', icon_type='fa', icon_value='fa-sitemap'))


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
    # 用于方便快捷的更新表设计
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@172.16.207.15:3306/apitest'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    db.app = app
    db.init_app(app)
    db.create_all()
