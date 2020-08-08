from flask import Flask, flash
from flask_babelex import Babel
from flask_sqlalchemy import SQLAlchemy
from database_data.case_model import db, admin


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@172.16.207.15:3306/apitest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'
db.init_app(app)
admin.init_app(app)
Babel(app)


if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True, port=8000)
