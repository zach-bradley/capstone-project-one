from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, Length, InputRequired

class UserAddForm(FlaskForm):
  """Form for adding users."""

  username = StringField('Username', validators=[DataRequired()])
  email = StringField('E-mail', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[Length(min=6)])

class EditUserForm(FlaskForm):
  """Form for editing user information"""

  username = StringField('Username', validators=[DataRequired()])
  email = StringField('E-mail', validators=[DataRequired(), Email()])
  name = StringField("Full Name")
  weight = IntegerField("Weight (in pounds)")
  password = PasswordField('Password', validators=[Length(min=6)])

class LoginForm(FlaskForm):
  """Form for logging a user in"""

  username = StringField("Username", validators=[InputRequired(message="Please enter a username")])
  password = PasswordField("Password", validators=[InputRequired(message="Please enter a password")])

class AddRecipeForm(FlaskForm):
  """Form for adding a recipe"""

  name = StringField("Recipe Name", validators=[InputRequired(message="Please enter a name for your recipe")])
  ingredients = TextAreaField("Ingredients. Put each ingredient on a new line", validators=[InputRequired(message="Please enter ingredients for your recipe")])