from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
 db.app=app
 db.init_app(app)

class User(db.Model):
  """Model for users"""

  __tablename__ = "users"
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  username = db.Column(db.Test, nullable=False, unique=True)
  password = db.Column(db.Text, nullable=False)
  email = db.Column(db.Text, nullable=False)
  recipes = db.relationship("Recipe")

  def __repr__(self):
  return f"<User #{self.id} {self.username}, {self.email}>"

  @classmethod
  def signup(cls, username, email, password, image_url):
      """Sign up user.Hashes password and adds user to system."""
      hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
      user = User(
          username=username,
          email=email,
          password=hashed_pwd,
          image_url=image_url,
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
  ingredients = db.relationship("Ingredient")

  def __repr__(self):
   return f"<Recipes {self.id} {self.name}>"

class Ingredient(db.Model):
  """Model for single ingredient"""

  __tablename__ = "ingredients"

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  amount = db.Column(db.Text, nullable=False)

  