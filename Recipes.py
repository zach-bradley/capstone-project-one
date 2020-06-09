from models import Recipe, Ingredient

class Recipes:
  """Methods for recipes"""
  def process_Recipe(name, user, response):
    """Converts data to whole numbers and returns Recipe model"""
    calories = round(response['calories']) if response['calories'] else 0 
    carbs=round(response['totalNutrients']['CHOCDF']['quantity'])
    fat=round(response['totalNutrients']['FAT']['quantity'])
    protein=round(response['totalNutrients']['PROCNT']['quantity'])
    return Recipe(name=name, calories=calories, carbs=carbs, fat=fat, protein=protein, user_id=user.id)

  def edit_Recipe_Data(recipe, name, response):
    """Converts data to whole numbers and sets recipe values to new values"""
    recipe.name = name
    recipe.calories = round(response['calories'])
    recipe.carbs=round(response['totalNutrients']['CHOCDF']['quantity'])
    recipe.fat=round(response['totalNutrients']['FAT']['quantity'])
    recipe.protein=round(response['totalNutrients']['PROCNT']['quantity'])
    return recipe.name, recipe.calories, recipe.carbs, recipe.fat, recipe.protein

  def set_Edit_Recipe_Info(form, recipe):
    """Sets the form for editing recipe with db data"""
    form.name.data = recipe.name
    ingr = [ingredient.amount for ingredient in recipe.ingredients]
    new_Line_Ingr = [ingredient + "\n" for ingredient in ingr]
    combined_Ingr = "".join(new_Line_Ingr)
    form.ingredients.data = combined_Ingr
    return form.name.data, form.ingredients.data  