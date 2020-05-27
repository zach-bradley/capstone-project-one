// "https://api.edamam.com/api/nutrition-details?app_id=${APP_ID}&app_key={APP_KEY}"
// title, ingr needed in json
const APP_ID = '0720c12f';
const APP_KEY = '2536f33f4e60d575d9e90d9c8012fe87';
const API_URL = 'https://api.edamam.com/api/nutrition-details';

$form = $("#addForm");

async function handleData(evt){
  evt.preventDefault()
  let name =  $("#name").val()
  let ingredients = $("#ingredients").val()
  let arrIngredients = ingredients.split(/\n/)

  console.log(arrIngredients)
  jsonToSend = {
    "title" : name,
    "ingr" : arrIngredients
  }
  let response = await axios.post(`https://api.edamam.com/api/nutrition-details?app_id=${APP_ID}&app_key=${APP_KEY}`, jsonToSend)
  let pulledData = {
    "name" : name,
    "ingredients" : arrIngredients,
    "calories" : Math.floor(response['data']['calories']),
    "carbs" : Math.floor(response['data']['totalNutrients']['CHOCDF']['quantity'])+"g",
    "fat" : Math.floor(response['data']['totalNutrients']['FAT']['quantity'])+"g",
    "protein" : Math.floor(response['data']['totalNutrients']['PROCNT']['quantity'])+"g"
  }
  console.log(pulledData)
}

$form.on("submit", handleData);