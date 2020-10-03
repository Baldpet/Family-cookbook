import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_login import LoginManager, UserMixin

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

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
    user.insert_one(request.form.to_dict())
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=int(
        os.environ.get('PORT')), debug=True)
