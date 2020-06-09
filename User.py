
class User_Methods:
  """Methods for manipulating user info"""
  def set_Edit_User_Info(form, user):
    form.username.data = user.username
    form.email.data = user.email
    form.name.data = user.name
    form.weight.data = user.weight
    return form.username.data, form.email.data, form.name.data, form.weight.data

  def edit_User_Info(form, user):
    """Sets new user information from form"""
    user.username = form.username.data
    user.email = form.email.data
    user.name = form.name.data
    user.weight = form.weight.data
    return user.username, user.email, user.name, user.weight
