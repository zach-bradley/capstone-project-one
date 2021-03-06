from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import User, Recipe, Ingredient, connect_db, db
from sqlalchemy.exc import IntegrityError
from forms import UserAddForm, LoginForm, RecipeForm, EditUserForm
from werkzeug.datastructures import MultiDict
from User import *
from Macro_Api_Caller import*
from Recipes import *
import requests
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
# db.drop_all()
# db.create_all()

@app.errorhandler(404)
def not_found(e):
  return render_template("404.html", classname="error"), 404

###########################
### Auth routes
###########################

@app.route("/")
def home_page():
  if 'username' in session:
    return redirect(f"/users/{session['username']}")
  else:  
    return render_template("homepage.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
  """Handle user signup."""
  form = UserAddForm()

  if form.validate_on_submit():
    try:
      user = User.signup(
          username=form.username.data,
          password=form.password.data,
          email=form.email.data,
      )
      db.session.commit()

    except IntegrityError:
      flash("Username already taken", 'danger')
      return render_template('/user/signup.html', form=form)

    session['username'] = user.username
    return redirect(f"/users/{user.username}")
  else:
      return render_template('/user/signup.html', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
  """Handle user login."""
  form = LoginForm()

  if form.validate_on_submit():
    user = User.authenticate(form.username.data, form.password.data)
    if user:
        session["username"] = user.username
        flash(f"Hello, {user.username}!", "success")
        return redirect(f"/users/{user.username}")
    else:
      flash("Invalid credentials.", 'danger')
      return redirect("/login")
  else:
    return render_template('/login.html', form=form)

@app.route("/logout")
def logout():
  session.pop('username')
  return redirect("/login")


###########################
### User routes
###########################

@app.route("/users/<username>")
def user_page(username):
  user = User.query.filter_by(username=username).first()
  User_Methods.check_username(username)
  return render_template("/user/user_page.html", user=user)

@app.route("/users/<username>/edit", methods=["GET", "POST"])
def edit_user(username):
  user = User.query.filter_by(username=username).first()
  form = EditUserForm()
  if form.validate_on_submit():
    user = User.authenticate(form.username.data, form.password.data)
    if user:
      User_Methods.edit_User_Info(form, user)
      db.session.add(user)
      db.session.commit()
      flash("Information updated!", "success")
      return redirect(f"/users/{user.username}")
    else:
      flash("Invalid credentials", "danger")
      return redirect(f"/users/{user.username}")
  else:
    User_Methods.set_Edit_User_Info(form, user)
    return render_template("/user/edit_user.html", form=form, user=user)

@app.route("/users/<username>/recipes/<int:recipe_id>")
def show_recipe(username, recipe_id):
  recipe = Recipe.query.get(recipe_id)
  net_carbs = int(recipe.carbs) - int(recipe.fiber)
  return render_template("/recipes/show_recipe.html", recipe=recipe, net_carbs=net_carbs)

@app.route("/users/<username>/delete")
def delete_user(username):
  if 'username' not in session:
    flash("You must be logged in to do that", "danger")
    return redirect("/login")
  user = User.query.filter_by(username=username).first()
  db.session.delete(user)
  db.session.commit()
  del session['username']
  return redirect("/login")

###########################
### Recipe routes
###########################

@app.route("/users/<username>/recipes")
def all_recipes(username):
  user = User.query.filter_by(username=username).first()
  return render_template("/recipes/all_recipes.html", user=user)

@app.route("/users/<username>/recipes/add", methods=["GET","POST"])
def add_recipe(username):
  user = User.query.filter_by(username=username).first()
  form = RecipeForm()
  if form.validate_on_submit():
    name = request.form['name'];
    image = request.form['recipe_image']
    ingredients = request.form['ingredients'].splitlines()
    response = Macro_Api_Caller.get_Data(Macro_Api_Caller, name, ingredients)
    if 'error' in response:
      flash("Ingredients not valid, make sure ingredients are on separate lines.", "danger")
      return redirect(f"/users/{session['username']}/recipes/add")
    else:
      recipe = Recipe_Factory.process_Recipe(name, image, user, response)
      db.session.add(recipe)
      db.session.commit()
      add_Ingredients = [Ingredient(amount=ingredient, recipe_id=recipe.id) for ingredient in ingredients]
      db.session.add_all(add_Ingredients)
      db.session.commit()
      flash("Recipe added successfully!", "success")
      return redirect(f"/users/{user.username}/recipes")
  else: 
    return render_template("/recipes/add_recipe.html", form=form, user=user)

@app.route("/users/<username>/recipes/<int:recipe_id>/edit", methods=["GET", "POST"])
def edit_recipe(username,recipe_id):
  user = User.query.filter_by(username=username).first()
  recipe = Recipe.query.get(recipe_id)
  form = RecipeForm()
  if form.validate_on_submit():
    delete_Ingr = Ingredient.query.filter_by(recipe_id=recipe.id).all()
    for ingr in delete_Ingr:
      db.session.delete(ingr)
    db.session.commit()
    name = request.form['name']
    recipe_image = request.form['recipe_image']
    ingredients = request.form['ingredients'].splitlines()
    response = Macro_Api_Caller.get_Data(name, ingredients)
    Recipe_Factory.edit_Recipe_Data(recipe, recipe_image, name, response)
    db.session.commit()
    add_Ingredients = [Ingredient(amount=ingredient, recipe_id=recipe.id) for ingredient in ingredients]
    db.session.add_all(add_Ingredients)
    db.session.commit()
    flash("Recipe updated!", "success")
    return redirect(f"/users/{user.username}/recipes/{recipe.id}")
  else:
    Recipe_Factory.set_Edit_Recipe_Info(form, recipe)
    return render_template("/recipes/edit_recipe.html", form=form, user=user, recipe=recipe)

@app.route("/users/<username>/recipes/<int:recipe_id>/delete")
def delete_recipe(username,recipe_id):
  user = User.query.filter_by(username=username).first()
  recipe = Recipe.query.get(recipe_id)
  db.session.delete(recipe)
  db.session.commit()
  flash("Recipe deleted!", "success")
  return redirect(f'/users/{user.username}/recipes')

