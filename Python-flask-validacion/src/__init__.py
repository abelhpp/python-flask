from flask import Flask
from flask_cors import CORS
from src.main import main
from src.config import Config
from src.user import user
from src.blog import blog
from src.extinsions import db, mongo, mail
from flask_pymongo import PyMongo
from flask_mail import Mail, Message


def create_app():

    app = Flask(__name__)

    app.config['MAIL_SERVER']='smtp.googlemail.com' #mail server
    app.config['MAIL_PORT'] = 587 #mail port
    app.config['MAIL_USERNAME'] = 'nuevoencuentrolist@gmail.com' #email
    app.config['MAIL_PASSWORD'] = 'eylmbqwynujhqabn' #password
    app.config['MAIL_USE_TLS'] = True #security type
    app.config['MAIL_USE_SSL'] = False #security type
    
    #app = Flask(__name__)
    #app.config.from_pyfile('config.cfg')
    mail.init_app(app)
    #db.init_app(app)
    
    app.config.from_object(config.ProductionConfig)
    #app=Flask(__name__)
    #app.config.from_object
    
    CORS(app)
    client = PyMongo(app)
    
    #app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(blog, url_prefix='/blog')
    app.register_blueprint(main)
    
    return app
