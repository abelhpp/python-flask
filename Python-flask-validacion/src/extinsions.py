from flask_pymongo import PyMongo
from pymongo import database
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

mail = Mail()

login_manager = LoginManager() 
login_manager.login_view = "user.login"
login_manager.login_message = "Please Login to access this page"
login_manager.login_message_category = "warning"


s = URLSafeTimedSerializer('Thisissecret')

mongo = PyMongo()


#msg = Message('Confirm Email', sender='anthony@prettyprinted.com', recipients=[email])

#link = url_for('confirm_email', token=token, _external=True)

