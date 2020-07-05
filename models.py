
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
 db.app=app
 db.init_app(app)

class User(db.Model):
  """Model for users"""

  __tablename__ = "users"
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  username = db.Column(db.Text, nullable=False, unique=True)
  password = db.Column(db.Text, nullable=False)
  email = db.Column(db.Text, nullable=False)
  name = db.Column(db.Text)
  weight = db.Column(db.Integer)
  user_image = db.Column(db.Text, default="/static/images/default_user_image.jpg")
  recipes = db.relationship("Recipe", backref="user")

  def __repr__(self):
    return f"<User #{self.id} {self.username}, {self.email}>"

  @classmethod
  def signup(cls, username, email, password):
      """Sign up user.Hashes password and adds user to system."""
      hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
      user = User(
          username=username,
          email=email,
          password=hashed_pwd,
      )

      db.session.add(user)
      return user

  @classmethod
  def authenticate(cls, username, password):
      """Find user with `username` and `password`.
       If can't find matching user (or if password is wrong), returns False.
      """
      user = cls.query.filter_by(username=username).first()
      if user:
          is_auth = bcrypt.check_password_hash(user.password, password)
          if is_auth:
              return user
      return False

class Recipe(db.Model):
  """Model for recipes"""

  __tablename__ = "recipes"
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.Text, nullable=False)
  calories = db.Column(db.Text)
  fat = db.Column(db.Text)
  carbs = db.Column(db.Text)
  protein = db.Column(db.Text)
  carbs_from = db.Column(db.Text)
  protein_from = db.Column(db.Text)
  fat_from = db.Column(db.Text)
  fiber = db.Column(db.Text)
  recipe_image = db.Column(db.Text, default="/static/images/default_recipe_image.jpg")
  user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
  ingredients = db.relationship("Ingredient", backref="recipe", cascade="all, delete-orphan")


  def __repr__(self):
   return f"<Recipes {self.id} {self.name}>"

class Ingredient(db.Model):
  """Model for single ingredient"""

  __tablename__ = "ingredients"

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  amount = db.Column(db.Text, nullable=False)
  recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False)

  