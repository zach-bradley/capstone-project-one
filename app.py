from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import User, Recipe, Ingredient, connect_db, db
from sqlalchemy.exc import IntegrityError
from forms import UserAddForm, LoginForm, AddRecipeForm
from werkzeug.datastructures import MultiDict

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///capstone_one'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'borkborkiamdog'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

# db.create_all()

@app.route("/")
def home_page():
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
    flash("Invalid credentials.", 'danger')

  return render_template('/login.html', form=form)

@app.route("/users/<username>")
def user_page(username):
  user = User.query.filter_by(username=username).first()
  return render_template("/user/user_page.html", user=user)

# @app.route("/<username>/recipes")
# def show_recipes(username):

# @app.route("/<username>/edit", methods=["GET", "POST"])
# def edit_user(username):

# @app.route("/<username>/delete")
# def delete_user(username):

@app.route("/users/<username>/recipes/add")
def add_recipe(username):
  user = User.query.filter_by(username=username).first()
  # data = MultiDict(mapping=request.json)
  # form = AddRecipeForm(data, meta={'csrf': False})
  return render_template("/recipes/add_recipe.html")

@app.route("/recipes/processing", methods=["POST"])
def add_recipe_processing():
  name = request.json['name']
  ingredients = request.json['ingr']
  return jsonify(ingredients)

# @app.route("/recipes/<int:recipe_id>/edit", methods=["GET", "POST"])
# def edit_recipe(recipe_job):

# @app.route("/recipes/<intrecipe_id>/delete")
# def delete_recipe(recipe_id):

@app.route("/logout")
def logout():
  session.pop("username")
  return redirect("/login")