import requests
from config import API_KEY, API_ID

class Macro_Api_Caller:
  """Methods for dealing with the api"""
  
  def serialize(name, ingredients):
    return {
      'title': name,
      'ingr' : ingredients
    }  

  def get_Data(self, name, ingr):
    to_send_data = self.serialize(name, ingr)
    api_data = requests.post(f"https://api.edamam.com/api/nutrition-details?app_id={API_ID}&app_key={API_KEY}", json = to_send_data)
    return api_data.json()


