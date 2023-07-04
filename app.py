import httplib2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from googleapiclient import discovery
import mammoth
from base2 import get_courses_html
import datetime
from base2 import get_courses_html, build_html, authorize_credentials, update_post
from twitter_api import twitter_auto
from flask import Flask, render_template, request
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import os
from datetime import date


secret_key = os.urandom(24)
print(secret_key)
import csv


today = date.today().strftime("%d-%B-%y")
title = f"UDEMY COURSES WITH FREE CERTIFICATE | {today} | IHTREEKTECHCOURSES"

# app = Flask(__name__)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = secret_key
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    message = db.Column(db.Text)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists and the password is correct
        user = User.query.filter_by(username=username).first()
        if user and password == user.password:
            login_user(user)  # Log in the user
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')


# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username is already taken
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('signup.html', error='Username already exists')

        # Create a new user
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)  # Log in the newly registered user
        return redirect(url_for('index'))

    return render_template('signup.html')

# Logout route

@app.route('/logout')
@login_required
def logout():
    logout_user()  # Log out the user
    return redirect(url_for('index'))

# Protected route example
@app.route('/protected')
@login_required
def protected():
    return 'This is a protected route. You can only access it if you are logged in.'


@app.route('/')
@login_required
def index():
    # return 'Welcome to the Flask app!'
    return render_template('index.html')


@app.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    if request.method == 'POST':
        # Get the submitted name from the form
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']

        form_data = FormData(name=name, email=email,phone=phone, message=message)
        db.session.add(form_data)
        db.session.commit()


        # Specify the post ID, blog ID, title, and content to update
        post_id = '8097252119400957177'
        blog_id = '5651255862571344247'
        test_post_id = '3359690114760599976'
        test_blog_id = '3481597162520342949'

        # Build HTML content from files
        html1 = build_html('first.html')
        html4 = "Updated Time (IST): " + datetime.datetime.now().strftime("%d/%m/%Y, %H:%M") + "\n"
        html2 = get_courses_html()
        html3 = build_html('file2.docx')
        all_html = html1 + html4 + html2 + html3

        # Get the current date


        content = all_html
        update_post(post_id, blog_id, title, content)
        # update_post(test_post_id, test_blog_id, title, content)

        return render_template('success.html')
    else:
        return render_template('failure.html')


from flask import request

@app.route('/admin', methods=['GET'])
@login_required
def admin():
    if request.method == 'GET':
        formdata = FormData.query.all()
        userdata = User.query.all()
        return render_template('admin.html', formdata=formdata, userdata=userdata)
    

@app.route('/tweet', methods=['GET'])
@login_required
def twitter():
    content_tweet = title + "Get Free Udemy Courses Daily " + "https://bit.ly/3oDp19M " + "#udemy #udemycoursesfree #udemycoupons #freecertificate #freecourseswithcertificates " 
    return twitter_auto(content_tweet)




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0",port=5000)

