import requests

class Macro_Api_Caller:
  """Methods for dealing with the api"""
  
  def serialize(name, ingredients):
    return {
      'title': name,
      'ingr' : ingredients
    }  

  def get_Data(self, name, ingr):
    to_send_data = self.serialize(name, ingr)
    api_data = requests.post(f"https://api.edamam.com/api/nutrition-details?app_id={process.env.API_ID}&app_key={process.env.API_KEY}", json = to_send_data)
    return api_data.json()


