from models import Recipe, Ingredient

class Recipe_Factory:
  """Methods for recipes"""
  def process_Recipe(name, image, user, response):
    """Converts data to whole numbers and returns Recipe model"""
    calories = round(response['calories']) if response['calories'] else 0 
    carbs=round(response['totalNutrients']['CHOCDF']['quantity'])
    fat=round(response['totalNutrients']['FAT']['quantity'])
    protein=round(response['totalNutrients']['PROCNT']['quantity'])
    fiber=round(response['totalNutrients']['FIBTG']['quantity'])
    carbs_from=round(response['totalNutrientsKCal']['CHOCDF_KCAL']['quantity'])
    fat_from=round(response['totalNutrientsKCal']['FAT_KCAL']['quantity'])
    protein_from=round(response['totalNutrientsKCal']['PROCNT_KCAL']['quantity'])
    recipe_img = image or Recipe.recipe_image.default.arg
    return Recipe(
      name=name, 
      calories=calories, 
      recipe_image=recipe_img, 
      carbs=carbs, 
      fat=fat, 
      protein=protein, 
      fiber=fiber,
      carbs_from=carbs_from, 
      protein_from=protein_from, 
      fat_from=fat_from,
      user_id=user.id)

  def edit_Recipe_Data(recipe, image, name, response):
    """Converts data to whole numbers and sets recipe values to new values"""
    recipe.name = name
    recipe.recipe_image = image or Recipe.recipe_image.default.arg
    recipe.calories = round(response['calories'])
    recipe.carbs=round(response['totalNutrients']['CHOCDF']['quantity'])
    recipe.fat=round(response['totalNutrients']['FAT']['quantity'])
    recipe.protein=round(response['totalNutrients']['PROCNT']['quantity'])
    return recipe.name, recipe.calories, recipe.carbs, recipe.fat, recipe.protein, recipe.recipe_image

  def set_Edit_Recipe_Info(form, recipe):
    """Sets the form for editing recipe with db data"""
    form.name.data = recipe.name
    form.recipe_image.data = recipe.recipe_image
    ingr = [ingredient.amount for ingredient in recipe.ingredients]
    new_Line_Ingr = [ingredient + "\n" for ingredient in ingr]
    combined_Ingr = "".join(new_Line_Ingr)
    form.ingredients.data = combined_Ingr
    return form.name.data, form.ingredients.data, form.recipe_image  