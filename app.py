import os
from flask import Flask, render_template, redirect, request, flash, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config["MONGO_DBNAME"] = 'recipe_hub'
app.config["MONGO_URI"] = 'mongodb://admin:s040793@ds229186.mlab.com:29186/recipe_hub'

mongo = PyMongo(app)

# MongoDB collections

users_collection = mongo.db.users
recipes_collection = mongo.db.recipes
categories_collection = mongo.db.categories

# Routes

@app.route('/', methods=["POST", "GET"])
def home():
    return render_template("home.html",
    recipes=mongo.db.recipes.find(),
    search_filter=mongo.db.categories.find())

@app.route('/login', methods=["POST", "GET"])
def login():
	if request.method == "POST":
		session['username'] = request.form["username"]
		
		if session['username'] == "":
			return render_template("login.html")
		else:
			return redirect("/loggedin/" + session['username'])
	return render_template("login.html")

    
@app.route('/loggedin/<username>', methods=["GET", "POST"])
def loggedin(username):
    return render_template(
    	"profile.html",
    	username=session['username'],
    	recipes=mongo.db.recipes.find( { "added_by" : session['username']})
    )

@app.route('/logout')
def logout():
	session.clear()
	flash('You were logged out!')
	return redirect(url_for('home'))    

@app.route('/add_recipe')
def add_recipe():
    return render_template("addrecipe.html",
    categories=mongo.db.categories.find())

@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    return redirect(url_for('loggedin'))

@app.route('/categories')
def categories():
    return render_template("categories.html",
    search_filter=mongo.db.categories.find(),
    categories=mongo.db.categories.find())

@app.route('/add_category')
def add_category():
    return render_template("addcategory.html",
    search_filter=mongo.db.categories.find())

@app.route('/insert_category', methods=['POST'])
def insert_category():
    categories = mongo.db.categories
    category_doc = {'category_name': request.form['category_name']}
    categories.insert_one(category_doc)
    return redirect(url_for('categories'))

@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    mongo.db.categories.remove({'_id': ObjectId(category_id)})
    return redirect(url_for('categories'))
    
@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('editcategory.html',
    category=mongo.db.categories.find_one({'_id': ObjectId(category_id)}),
    search_filter=mongo.db.categories.find())

    
@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    mongo.db.categories.update(
        {'_id': ObjectId(category_id)},
        {'category_name': request.form['category_name']})
    return redirect(url_for('categories'))
    
@app.route('/recipe')
def recipe():
    return render_template("recipe.html")
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)
