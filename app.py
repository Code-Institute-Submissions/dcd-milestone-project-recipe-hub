import os
from flask import Flask, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo, pymongo
from bson.objectid import ObjectId
from flask_bcrypt import bcrypt

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config['MONGO_DBNAME'] = 'recipe_hub'
app.config['MONGO_URI'] = "mongodb://admin:s040793@ds229186.mlab.com:29186/recipe_hub"

mongo = PyMongo(app)

# MongoDB collections

users_collection = mongo.db.users
recipes_collection = mongo.db.recipes
categories_collection = mongo.db.categories

# Variables

default_image = \
    'https://zabas.com/wp-content/uploads/2014/06/placeholder-food-hover.png'


# Routes

@app.route('/', methods=['POST', 'GET'])
def home():
    categories = list(categories_collection.find())
    recipes = recipes_collection.find().sort('name', pymongo.ASCENDING)
    return render_template('home.html',
                           recipes=recipes,
                           categories=categories)


@app.route('/<category_name>', methods=['GET'])
def filter_list(category_name):
    categories = list(categories_collection.find())
    category_name = categories_collection.find_one(
        {'category_name': category_name})
    recipes = recipes_collection.find()
    return render_template(
        'filter.html',
        categories=categories,
        category_name=category_name,
        recipes=recipes)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        existing_user = users_collection.find_one(
            {'name': request.form.get('username')})
        if existing_user:
            session['username'] = request.form.get('username')
            return redirect('/loggedin/' + session['username'])
        return redirect(url_for('signup'))
    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        existing_user = \
            users_collection.find_one(
                {'name': request.form.get('username')})
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form.get('password')
                                     .encode('utf-8'), bcrypt.gensalt())
            users_collection.insert(
                {'name': request.form.get('username'), 'password': hashpass})
            session['username'] = request.form.get('username')
            return redirect('/loggedin/' + session['username'])
    return render_template('signup.html')


@app.route('/loggedin/<username>', methods=['GET', 'POST'])
def loggedin(username):
    recipes = \
        recipes_collection.find({'added_by': session['username']})\
        .sort('name', pymongo.ASCENDING)
    return render_template(
        'profile.html',
        username=session['username'],
        recipes=recipes
        )


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route('/add_recipe')
def add_recipe():
    return render_template('addrecipe.html',
                           categories=categories_collection.find())


@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes = recipes_collection
    recipes.insert_one({
        'category': request.form.get('category_name'),
        'name': request.form.get('name'),
        'cooking_time': request.form.get('cooking'),
        'prep_time': request.form.get('prep'),
        'serves': request.form.get('serves'),
        'image': default_image,
        'added_by': session['username'],
        'ingredients': request.form.getlist('ingredient'),
        'method': request.form.get('method'),
        'cuisine': request.form.get('cuisine'),
        })
    return redirect(url_for('loggedin', username=session['username']))


@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    recipe = recipes_collection.find_one({'_id': ObjectId(recipe_id)})
    _categories = categories_collection.find()
    category_list = [category for category in _categories]
    return render_template('editrecipe.html', recipe=recipe,
                           categories=category_list)


@app.route('/update_recipe/<recipe_id>', methods=['POST'])
def update_recipe(recipe_id):
    recipes_collection.update({'_id': ObjectId(recipe_id)}, {
        'category': request.form.get('category_name'),
        'name': request.form.get('name'),
        'cooking_time': request.form.get('cooking'),
        'prep_time': request.form.get('prep'),
        'image': default_image,
        'serves': request.form.get('serves'),
        'ingredients': request.form.getlist('ingredient'),
        'method': request.form.get('method'),
        'cuisine': request.form.get('cuisine'),
        'added_by': session['username'],
        })
    return redirect(url_for('loggedin', username=session['username']))


@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    recipes_collection.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('loggedin', username=session['username']))


@app.route('/recipe/<recipe_id>')
def recipe(recipe_id):
    recipe = recipes_collection.find_one({'_id': ObjectId(recipe_id)})
    return render_template('recipe.html', recipe=recipe)


@app.route('/categories')
def categories():
    categories = \
        categories_collection.find().sort('category_name', pymongo.ASCENDING)
    return render_template('categories.html',
                           categories=categories)


@app.route('/add_category')
def add_category():
    return render_template('addcategory.html')


@app.route('/insert_category', methods=['POST'])
def insert_category():
    category_doc = {'category_name': request.form['category_name']}
    categories_collection.insert_one(category_doc)
    return redirect(url_for('categories'))


@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    categories_collection.remove({'_id': ObjectId(category_id)})
    return redirect(url_for('categories'))


@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('editcategory.html',
                           category=categories_collection.find_one(
                               {'_id': ObjectId(category_id)}
                               ))


@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    categories_collection.update(
        {'_id': ObjectId(category_id)},
        {'category_name': request.form['category_name']})
    return redirect(url_for('categories'))


if __name__ == '__main__':
    app.run(
        host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)
