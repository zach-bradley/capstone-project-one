import requests
import os

class Macro_Api_Caller:
  """Methods for dealing with the api"""
  
  def serialize(name, ingredients):
    return {
      'title': name,
      'ingr' : ingredients
    }  

  def get_Data(self, name, ingr):
    to_send_data = self.serialize(name, ingr)
    api_data = requests.post(f"https://api.edamam.com/api/nutrition-details?app_id={os.environ.get('API_ID')}&app_key={os.environ.get('API_KEY')}", json = to_send_data)
    return api_data.json()


