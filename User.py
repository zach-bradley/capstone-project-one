from flask import session, abort
from models import User

class User_Methods:
  """Methods for manipulating user info"""

  def check_username(username):
    """Check to see if username matches session"""
    if username != session['username'] or username is None:
      abort(404)

  def set_Edit_User_Info(form, user):
    """Set form with user information"""
    form.username.data = user.username
    form.email.data = user.email
    form.name.data = user.name
    form.weight.data = user.weight
    form.user_image.data = user.user_image
    return form.username.data, form.email.data, form.name.data, form.weight.data, form.user_image

  def edit_User_Info(form, user):
    """Sets new user information from form"""
    user.username = form.username.data
    user.email = form.email.data
    user.name = form.name.data
    user.weight = form.weight.data
    user.user_image = form.user_image.data or User.user_image.default.arg
    return user.username, user.email, user.name, user.weight, user.user_image
