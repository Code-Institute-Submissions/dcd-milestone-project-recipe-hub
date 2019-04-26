import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'recipe_hub'
app.config["MONGO_URI"] = 'mongodb://admin:s040793@ds229186.mlab.com:29186/recipe_hub'

mongo = PyMongo(app)

@app.route('/')
def home():
    return render_template("home.html",
    recipes=mongo.db.recipes.find())

@app.route('/login')
def login():
    return render_template("login.html")
    
@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/add_recipe')
def add_recipe():
    return render_template("addrecipe.html")

@app.route('/categories')
def categories():
    return render_template("categories.html",
    recipes=mongo.db.recipes.find())

@app.route('/add_category')
def add_category():
    return render_template("addcategory.html")
    
@app.route('/recipe')
def recipe():
    return render_template("recipe.html")

@app.route('/get_recipes')
def get_recipes():
    return render_template("getrecipes.html",
    recipes=mongo.db.recipes.find())

    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)
