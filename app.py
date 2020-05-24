from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///capstone_one'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'borkborkiamdog'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route("/")
def home_page():
 return render_template("home.html")

@app.route("/signup", methods=["GET, POST"])
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
      return render_template('signup.html', form=form)

    session['user_id'] = user.id
    return redirect("/")
  else:
      return render_template('signup.html', form=form)

@app.route("/login", methods=["GET, POST"])
def login():
  """Handle user login."""

  form = LoginForm()

  if form.validate_on_submit():
    user = User.authenticate(form.username.data, form.password.data)

    if user:
        session["user_id"] = user.id
        flash(f"Hello, {user.username}!", "success")
        return redirect("/login")
    flash("Invalid credentials.", 'danger')

  return render_template('/login.html', form=form)

@app.route("/<username>")
def user_page(username):
  user = User.query.filter_by(username).first()
  return render_template("user_page.html", user=user)

@app.route("/<username>/recipes")
def show_recipes(username):

@app.route("/<username>/edit", methods=["GET", "POST"])
def edit_user(username):

@app.route("/<username>/delete")
def delete_user(username):

@app.route("/recipes/add_recipe", methods=["GET", "POST"])
def add_recipe():

@app.route("/recipes/<int:recipe_id>/edit", methods=["GET", "POST"])
def edit_recipe(recipe_job):

@app.route("/recipes/<intrecipe_id>/delete")
def delete_recipe(recipe_id):

@app.route("/logout")
def logout():
  session.pop("user_id")
  return redirect("/login")