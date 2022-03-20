from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

my_app = Flask(__name__)
my_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
my_app.config['SECRET_KEY'] = '12345'
db = SQLAlchemy(my_app)
migrate = Migrate(my_app, db)
login = LoginManager(my_app)
login.login_view = 'login'
admin = Admin(my_app, name='my_app', template_mode='bootstrap3')

from app import routes, models

admin.add_view(ModelView(models.User, db.session))
