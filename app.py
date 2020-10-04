import os
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
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

login_manager.login_view = "home"

"""
Flask-Login User Class and callback function
Code taken from Slack Issac posted on October 1 2019
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
End of code taken from Slack user Issac
"""


@app.route('/')
def home():
    """
        route to the home page with no login,
        redirects to personal home if already logged in
    """
    if current_user.is_authenticated:
        return redirect(url_for('home_login', username=current_user))
    return render_template("index.html")


@app.route('/signup')
def sign_up():
    # route to the sign up form
    return render_template("signup.html")


@app.route('/home/<username>')
@login_required
def home_login(username):
    # route to the home section for logged in users
    return render_template('homelogin.html')


@app.route('/add-recipe')
@login_required
def add_recipe():
    # route to the form to add a recipe to the app
    return render_template('addrecipe.html')


@app.route('/find-a-recipe')
@login_required
def search_recipes():
    # route to the page to search for other recipes on the app
    return render_template('searchrecipes.html')


@app.route('/mycookbook/<username>')
@login_required
def my_cookbook(username):
    # route to the cookbook of the user, shows the recipes they have saved
    return render_template('mycookbook.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    """
        Authenticates the login with the database
        Uses the hashed password and username to authenticate
        Once done, logs user in a redirects to their home
        If not authenticated will return to login form
    """
    if request.method == 'POST':
        lowerUsername = request.form.get('username').lower()
        user = mongo.db.users.find_one(
            {"username": lowerUsername})
        print(user)
        if user is not None:
            userPassword = check_password_hash(
                user['password'], request.form.get('password'))
            if user and userPassword:
                user_obj = User(user['username'])
                login_user(user_obj)
                flash("Logged in successfully")
                print(User)
                return redirect(request.args.get("next") or url_for(
                    "home_login", username=user['username']))
        flash("Wrong username or password")
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    """
        Logout function for users that are logged in
    """
    logout_user()
    return redirect(url_for('home'))


@app.route('/signup/user', methods=['POST', 'GET'])
def sign_up_user():
    """
        Sign up form
        Will check if the user or the email has already been used
        Will check that the password has been typed correctly
        Will then add the user to the database
        Redirects to the login page
    """
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
