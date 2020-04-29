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
 name = db.Column(db.Text)

 def __repr__(self):
  return f"<User {self.id} {self.username} {self.password} {self.name}>"

class Recipe(db.Model):
 """Model for recipes"""

 __tablename__ = "recipes"
 id = db.Column(db.Integer, primary_key=True, autoincrement=True)
 name = db.Column(db.Text, nullable=False)
 ingredients = db.Column(db.Text, nullable=False)
 macro_count = db.Column(db.Text)


 def __repr__(self):
  return f"<Recipes {self.id} {self.name} {self.ingredients} {self.macro_count}>"

  