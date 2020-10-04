import os
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_login import LoginManager, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

if os.path.exists("env.py"):
    import env

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config["MONGO_DBNAME"] = 'family_cookbook'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')

login_manager = LoginManager()

mongo = PyMongo(app)

login_manager.init_app(app)

"""
Flask-Login User Class and callback function
Code taken from Slack Issac October 1 2019
"""


class User():
    def __init__(self, username):
        self.username = username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username


@login_manager.user_loader
def load_user(username):
    u = mongo.db.users.find_one({"username": username})
    if not u:
        return None
    return User(u['username'])


"""
End of code taken from Slack
"""


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/SignUp')
def sign_up():
    return render_template("signup.html")


@app.route('/home/<username>')
def home_login(username):
    return render_template('homelogin.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        lowerUsername = request.form.get('username').lower()
        user = mongo.db.users.find_one(
            {"username": lowerUsername})
        print(user)
        userPassword = check_password_hash(
            user['password'], request.form.get('password'))
        if user and userPassword:
            user_obj = User(user['username'])
            login_user(user_obj)
            flash("Logged in successfully")
            return redirect(request.args.get("next") or url_for(
                "home_login", username=user['username']))
        flash("Wrong username or password")
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/SignUp/user', methods=['POST', 'GET'])
def sign_up_user():
    user = mongo.db.users
    usernameCheck = user.find({'username': (request.form.get(
        'username')).lower()}).count()
    emailCheck = user.find({'email': (request.form.get(
        'email')).lower()}).count()
    if usernameCheck == 1:
        flash('Username already taken')
    else:
        if emailCheck == 1:
            flash('Email address already has a profile')
        else:
            if (request.form.get('password')) == (request.form.get(
                    'password_check')):
                hash = generate_password_hash(request.form.get('password'))
                user.insert_one({
                    'username': request.form.get('username').lower(),
                    'first_name': request.form.get('first_name').lower(),
                    'email': request.form.get('email').lower(),
                    'password': hash
                })
                return redirect(url_for('home'))
            else:
                flash('Error! Your password does not match')
    return redirect(url_for('sign_up'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=int(
        os.environ.get('PORT')), debug=True)
