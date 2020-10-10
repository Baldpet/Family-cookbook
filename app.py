import os
import datetime
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
        return redirect(url_for('home_login', username=current_user.username))
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


@app.route('/add-recipe', methods=['POST', 'GET'])
@login_required
def add_recipe():
    # route to the form to add a recipe to the app
    return render_template('addrecipe.html',
                           ingredients=mongo.db.main_ingredients.find())


@app.route('/add-recipe/submit', methods=['POST', 'GET'])
def add_recipe_form():
    '''
        Form to submit a new recipe to the database
    '''
    if request.method == 'POST':
        recipe = mongo.db.recipes
        recipe.insert_one({
            'recipe_name': request.form.get('recipe_name').lower(),
            'main_ingredient': request.form.get('main_ingredient'),
            'ingredients': request.form.getlist('ingredients'),
            'serves': request.form.get('serves'),
            'time': request.form.get('time'),
            'method': request.form.getlist('method'),
            'time_stamp': datetime.datetime.now(),
            'original_user': current_user.username,
            'cookbook': [current_user.username],
            'love': 0,
            'original': True
        })
        flash('submitted')
    return redirect(url_for('add_recipe'))


@app.route('/find-a-recipe', methods=['POST', 'GET'])
@login_required
def search_recipes():
    # route to the page to search for other recipes on the app
    return render_template('searchrecipes.html',
                           recipes=mongo.db.recipes.find({'original': True}),
                           ingredients=mongo.db.main_ingredients.find())


@app.route('/find-a-recipe/<recipe>/<love>')
def add_cookbook(recipe, love):
    '''
    adds the recipe from the search menu to the user's cookbook.
    also adds another number on to the love list for the orignal user.
    '''
    recipe_id = ObjectId(recipe)
    numberAdd = int(love) + 1
    mongo.db.recipes.update_one(
        {"_id": recipe_id},
        {'$push': {'cookbook': current_user.username}}
    )
    mongo.db.recipes.update_one(
        {"_id": recipe_id},
        {'$set': {"love": numberAdd}}
    )
    return redirect(url_for('search_recipes'))


@app.route('/mycookbook/<username>')
@login_required
def my_cookbook(username):
    # route to the cookbook of the user, shows the recipes they have saved
    return render_template('mycookbook.html',
                           recipes=mongo.db.recipes.find({
                               'cookbook': username}),
                           ingredients=mongo.db.main_ingredients.find())


@app.route('/amend/<recipeID>', methods=['POST', 'GET'])
@login_required
def recipe_amend(recipeID):
    '''
        route to the amend recipe page,
        which will automatically fill in the various fields
    '''
    recipe = ObjectId(recipeID)
    return render_template('recipeamend.html',
                           ingredients=mongo.db.main_ingredients.find(),
                           recipe=mongo.db.recipes.find({'_id': recipe}))


@app.route('/amended/<recipeID>/<recipe_name>/<main_ingredient>/<serves>/<time>/<ingredients>/<method>', methods=['POST', 'GET'])
@login_required
def add_recipe_amend(recipeID, recipe_name, main_ingredient, serves, time, ingredients, method):
    database = mongo.db.recipes
    recipe = ObjectId(recipeID)
    amended_recipe_name = request.form.get('recipe_name').lower()
    amended_main_ingredient = request.form.get('main_ingredient').lower()
    amended_serves = request.form.get('serves')
    amended_time = request.form.get('time')
    amended_ingredients = request.form.getlist('ingredients')
    amended_method = request.form.getlist('method')
    if request.method == 'POST':
        if recipe_name == amended_recipe_name and main_ingredient == amended_main_ingredient and serves == amended_serves and time == amended_time and ingredients == amended_ingredients and method == amended_method:
            flash('unsucessful, not amendments were made')
            return redirect(url_for('recipe_amend', recipeID=recipeID))
        else:
            cookbook_array = database.find({'_id': recipe})
            cookbook_array_len = len(cookbook_array[0]['cookbook'])
            if cookbook_array_len == 1 and not cookbook_array[0]['original']:
                database.delete_one({'_id': recipe})
            else:
                database.update({'_id': recipe},
                                {'$pull': {'cookbook': current_user.username}})
            database.insert_one({
                'recipe_name': request.form.get('recipe_name').lower(),
                'main_ingredient': request.form.get('main_ingredient'),
                'ingredients': request.form.getlist('ingredients'),
                'serves': request.form.get('serves'),
                'time': request.form.get('time'),
                'method': request.form.getlist('method'),
                'time_stamp': datetime.datetime.now(),
                'original_user': current_user.username,
                'cookbook': [current_user.username],
                'love': 0,
                'original': False
            })
    return redirect(url_for('my_cookbook', username=current_user.username))


@app.route('/remove-cookbook/<recipeID>')
@login_required
def remove_cookbook(recipeID):
    recipe = ObjectId(recipeID)
    mongo.db.recipes.update({'_id': recipe},
                            {'$pull': {'cookbook': current_user.username}})
    return redirect(url_for('my_cookbook', username=current_user.username))


@app.route('/myuploaded/<username>')
@login_required
def my_uploaded(username):
    # route to the users uploaded recipes, where they can manage them
    return render_template('uploadedrecipes.html',
                           recipes=mongo.db.recipes.find({
                               'orignal_user': username}),
                           ingredients=mongo.db.main_ingredients.find())


@app.route('/recipe/<recipe>/<name>')
@login_required
def recipe(recipe, name):
    '''
        Will render the recipe template of the selected recipe.
    '''
    recipeID = ObjectId(recipe)
    return render_template('recipe.html',
                           recipe=mongo.db.recipes.find({
                               '_id': recipeID}))


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
        if user is not None:
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


def date_check(date):
    time_since_upload = datetime.datetime.now() - date

    if time_since_upload.days < 7:
        return True
    else:
        return False


app.jinja_env.globals.update(date_check=date_check)


def in_cookbook(cookbook, username):
    if username in cookbook:
        return True
    else:
        return False


app.jinja_env.globals.update(in_cookbook=in_cookbook)

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=int(
        os.environ.get('PORT')), debug=True)
