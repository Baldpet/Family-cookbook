import os
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

if os.path.exists("env.py"):
    import env

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config["MONGO_DBNAME"] = 'family_cookbook'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
'''
login_manager = LoginManager()
'''
mongo = PyMongo(app)
'''
login_manager.init_app(app)
'''

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/SignUp')
def sign_up():
    return render_template("signup.html")


@app.route('/SignUp/user', methods=['POST', 'GET'])
def sign_up_user():
    user = mongo.db.users
    usernameCheck = user.find({'username': (request.form.get(
        'username')).lower()}).count()
    if usernameCheck == 1:
        flash('Username already taken')
    else:
        if (request.form.get('password')) == (request.form.get(
                'password_check')):
            hash = generate_password_hash(request.form.get('password'))
            print(hash)
        else:
            flash('Error! Your password does not match')
    return redirect(url_for('sign_up'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=int(
        os.environ.get('PORT')), debug=True)
