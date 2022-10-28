from src.user import user
from flask import request, jsonify, Blueprint, abort
from flask_pymongo  import ObjectId, MongoClient
from jwt import encode
from datetime import datetime
from flask_login import login_user, logout_user, current_user, login_required
import hashlib

connection_str = 'mongodb://localhost:27017/myDatabase'
client = MongoClient(connection_str)
db = client.blogApp.user



# Hashing
def hash_str(str):
    return hashlib.sha256(str.encode()).hexdigest()

#Significa 'http://localhost:5000/user/new'

# If user exist
def existing_user(user):
    return True if db.find_one({'user' : user}) else False


@user.route('/new', methods = ['POST'])
def new_user():
    user = request.json['user']
    password = hash_str(request.json['password'])
    name = request.json['name']
    # User comprobations
    if user == None or password == None or name == None or user == '' or request.json['password'] == '' or name == '':
        abort(400,'{"message":"custom error message to appear in body"}') # Missing values
    if existing_user(user):
        abort(400,'{"message":"custom error message to appear in body"}') # User exist
    id = db.insert_one({
        'user' : user,
        'password' : password,
        'date' : datetime.today(),
        'name' : name
    })
    
    return jsonify({
        '_id': str(ObjectId(id.inserted_id))
    })


@user.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return 'you need to logout to access this page'
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()
        if user and user.check_password(form.password.data) :
            login_user(user, remember=True)
            return redirect(url_for('main.home'))
    return render_template('login.html', form=form)

""" @user.route('/login', methods = ['POST'])
def login():
    user = request.json['user']
    password = hash_str(request.jason['password'])

    original_user = db.find_one({'user': user})

    if original_user.password  != password:
        abort(400)
    else:
        return jsonify({
            'token': encode({
                'user': original_user['user'],
                'date': original_user['date']
            }, 'SECRET PASSWORD')
        }) 
        encode()  """