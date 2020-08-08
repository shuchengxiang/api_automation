from flask import flash
from gettext import gettext
from flask_admin import Admin
from flask_admin.actions import action
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Slice(db.Model):
    __tablename__ = 'apitest_case'

    id = db.Column(db.Integer, primary_key=True)
    case_name = db.Column(db.String(1024), unique=False, nullable=False)
    method = db.Column(db.String(1024), unique=False, nullable=False)
    url = db.Column(db.String(1024), unique=False, nullable=False)
    depending_case = db.Column(db.String(1024), unique=False, nullable=True)
    isrun = db.Column(db.String(1024), unique=False, nullable=True)
    params = db.Column(db.String(4096), unique=False, nullable=False)
    headers = db.Column(db.String(4096), unique=False, nullable=True)
    depending_teardowncase = db.Column(db.String(1024), unique=False, nullable=True)
    teardown_case = db.Column(db.String(1024), unique=False, nullable=True)
    status_code = db.Column(db.String(1024), unique=False, nullable=True)
    expect_result = db.Column(db.String(1024), unique=False, nullable=False)
    msg = db.Column(db.String(1024), unique=False, nullable=True)

    def import_slice(self):
        print("import")
        return True


class SliceView(ModelView):
    # 指定模板
    list_template = 'AdminLTE/list.html'
    create_template = 'AdminLTE/create.html'
    edit_template = 'AdminLTE/edit.html'
    details_template = 'AdminLTE/details.html'

    column_display_pk = True
    column_labels = {
        'id': 'ID',
        'case_name': '名称'
    }
    column_searchable_list = ['case_name']
    column_filters = ['case_name']
    can_view_details = True
    can_export = True
    export_types = ['csv', 'xls', 'json', 'html']
    can_set_page_size = True

    @action('import', '导入', '是否导入数据？')
    def action_import(self, ids):
        try:
            count = 0
            query = Slice.query.filter(Slice.id.in_(ids))
            for s in query.all():
                result = s.import_slice()
                if not result:
                    raise Exception('Empty data')
                else:
                    count += 1
            flash('数据源成功导入！')
        except Exception as ex:
            if not self.handle_view_exception(ex):
                raise
            flash(gettext('Failed to import slices. %s' % str(ex)), 'error')

admin = Admin(name='adminLTE', template_mode='bootstrap3', base_template='AdminLTE/mylayout.html', )  # 指定模板
admin.add_view(SliceView(Slice, db.session, name='数源管理', menu_icon_type='fa', menu_icon_value='fa-table'))
admin.add_link(MenuLink(name='模型图谱', url='#', icon_type='fa', icon_value='fa-sitemap'))


