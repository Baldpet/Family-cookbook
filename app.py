import os
import datetime
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_login import LoginManager, login_user, logout_user
from flask_login import current_user, login_required
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


@app.errorhandler(404)
def page_not_found(e):
    # route handling 404 error on a missing URL
    return render_template('404.html'), 404


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
        flash('Recipe Submitted! Feel free to add another.')
    return redirect(url_for('add_recipe'))


@app.route('/find-a-recipe', methods=['POST', 'GET'])
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
@app.route('/mycookbook/')
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


@app.route('/amended/<recipeID>', methods=['POST', 'GET'])
@login_required
def add_recipe_amend(recipeID):
    """
        If the recipe has changed it will check to see how many
        users are in the cookbook, if
        there are only 1 user and it is not an original
        recipe then it will delete the recipe in the database
        to keep the documents in the database low.

        The new recipe is then entered into the database as a 'non-original'.
        This recipe only appears in the
        users cookbook and does not appear
        to any other users in the search recipes.
    """
    database = mongo.db.recipes
    recipe = ObjectId(recipeID)
    if request.method == 'POST':
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


@app.route('/remove-cookbook/<recipeID>/<love>')
@login_required
def remove_cookbook(recipeID, love):
    """
    Removes the user from the cookbook of the recipe,
    they no longer can see the recipe in their cookbook
    Also reduces the 'love' number so that the tracking is acurate.
    """
    recipe = ObjectId(recipeID)
    numberSub = int(love) - 1
    mongo.db.recipes.update({'_id': recipe},
                            {'$pull': {'cookbook': current_user.username}})
    mongo.db.recipes.update({'_id': recipe},
                            {'$set': {"love": numberSub}})
    return redirect(url_for('my_cookbook', username=current_user.username))


@app.route('/myuploaded/<username>')
@login_required
def my_uploaded(username):
    # route to the users uploaded recipes, where they can manage them
    return render_template('uploadedrecipes.html',
                           recipes=mongo.db.recipes.find({
                               '$and': [{'original_user': username},
                                        {'original': True}]}),
                           ingredients=mongo.db.main_ingredients.find())


@app.route('/removerecipe/<recipeID>')
@login_required
def remove_recipe(recipeID):
    """
    Removes the recipe off the database.
    Can only be done if not in any other user cookbook
    This is checked on the HTML through an if statement
    """
    recipe = ObjectId(recipeID)
    mongo.db.recipes.delete_one({'_id': recipe})
    return redirect(url_for('my_uploaded', username=current_user.username))


@app.route('/recipe/<recipe>/<name>')
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
                return redirect(request.args.get("next") or url_for(
                    "home_login", username=user['username']))
        flash("Wrong Username or Password entered, please try again.")
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
                user_obj = User(request.form.get('username').lower())
                login_user(user_obj)
                return redirect(url_for('home'))
            else:
                flash('Error! Your password does not match')
    return redirect(url_for('sign_up'))


def date_check(date):
    """
    Checks to see how long ago the recipe was uploaded.
    If the recipe was less than 7 days returns True.
    """
    time_since_upload = datetime.datetime.now() - date

    if time_since_upload.days < 7:
        return True
    else:
        return False


app.jinja_env.globals.update(date_check=date_check)


def in_cookbook(cookbook, username):
    """
    Checks to see if the user is in a cookbook.
    If they are then it returns True.
    """
    if username in cookbook:
        return True
    else:
        return False


app.jinja_env.globals.update(in_cookbook=in_cookbook)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=int(
        os.environ.get('PORT')), debug=False)
