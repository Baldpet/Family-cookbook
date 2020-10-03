import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_login import LoginManager

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'family_cookbook'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
login_manager = LoginManager()

mongo = PyMongo(app)
login_manager.init_app(app)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/SignUp')
def sign_up():
    return render_template("signup.html")


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=int(
        os.environ.get('PORT')), debug=True)
