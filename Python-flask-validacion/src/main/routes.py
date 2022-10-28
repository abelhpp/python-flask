from src.main import main
from flask import Flask, render_template, request, url_for
from src.extinsions import s, mail
from src.user.models import User
from flask_mail import Mail, Message
import os



@main.route('/')
def index():
    
    
    #email = request.form['email']
    #token = s.dumps(email, salt='email-confirm')
    #msg = Message('Confirm Email', sender='nuevoencuentrolist@gmail.com', recipients=[email])
    #link = url_for('main.confirm_email', token=token, _external=True)
    #msg.body = 'Your link is {}'.format(link)
    #mail.send(msg)
    #'<h1>The email you entered is {}. The token is {}</h1>'.format(email, token)
    return render_template('index.html') 

@main.route('/confirm_email/<token>', methods = ['GET', 'POST'])
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except SignatureExpired:
        return "<h1>the token is expered</h1>"
    
    return 'The token works! '