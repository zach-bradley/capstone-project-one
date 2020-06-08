import requests
from models import Recipe, Ingredient

def serialize(name, ingredients):
  return {
    'title': name,
    'ingr' : ingredients
  }

def set_Edit_Recipe_Info(form, recipe):
  form.name.data = recipe.name
  ingr = [ingredient.amount for ingredient in recipe.ingredients]
  new_Line_Ingr = [ingredient + "\n" for ingredient in ingr]
  combined_Ingr = "".join(new_Line_Ingr)
  form.ingredients.data = combined_Ingr
  return form.name.data, form.ingredients.data
  
def process_Recipe(name, user, response):
  calories = round(response['calories']) if response['calories'] else 0 
  carbs=round(response['totalNutrients']['CHOCDF']['quantity'])
  fat=round(response['totalNutrients']['FAT']['quantity'])
  protein=round(response['totalNutrients']['PROCNT']['quantity'])
  return Recipe(name=name, calories=calories, carbs=carbs, fat=fat, protein=protein, user_id=user.id)

def get_Data(name, ingr):
    to_send_data = serialize(name, ingr)
    api_data = requests.post("https://api.edamam.com/api/nutrition-details?app_id=0720c12f&app_key=2536f33f4e60d575d9e90d9c8012fe87", json = to_send_data)
    return api_data.json()

def edit_Recipe_Data(recipe, name, response):
  recipe.name = name
  recipe.calories = round(response['calories'])
  recipe.carbs=round(response['totalNutrients']['CHOCDF']['quantity'])
  recipe.fat=round(response['totalNutrients']['FAT']['quantity'])
  recipe.protein=round(response['totalNutrients']['PROCNT']['quantity'])
  return recipe.name, recipe.calories, recipe.carbs, recipe.fat, recipe.protein

def set_Edit_User_Info(form, user):
  form.username.data = user.username
  form.email.data = user.email
  form.name.data = user.name
  form.weight.data = user.weight
  return form.username.data, form.email.data, form.name.data, form.weight.data