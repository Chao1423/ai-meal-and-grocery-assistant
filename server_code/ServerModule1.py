import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.http
import json

@anvil.server.callable
def suggest_meals(ingredients, allergies="", vegan_pref=False):
  """Call DeepSeek to get meals, recipes, and extra ingredients as JSON."""
  row = app_tables.config.get(name='DEEPSEEK_API_KEY')
  if not row:
    return [{"food_name": "Error", "recipe": "Missing API key", "to_buy": "", "link": ""}]
  api_key = row['value']

  headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
  }

  vegan_note = "The user prefers vegan meals." if vegan_pref else "Non-vegan options are acceptable."
  allergy_note = f" Avoid ingredients related to these allergies: {allergies}." if allergies else ""

  body = {
    "model": "deepseek-chat",
    "max_tokens": 500,
    "messages": [
      {"role": "system", "content": "You are a helpful cooking assistant."},
      {"role": "user", "content": f"""
I currently have these ingredients: {ingredients}.
{vegan_note}{allergy_note}

Please respond strictly as **valid JSON**, formatted as a list of objects.
Each object must have:
- food_name (string)
- recipe (short preparation description)
- to_buy (missing ingredients to purchase)
- link (a real or placeholder URL for the recipe)

Example:
[
  {{
    "food_name": "Vegan Fried Rice",
    "recipe": "Stir-fry rice with tofu and vegetables.",
    "to_buy": "Soy sauce, sesame oil",
    "link": "https://www.allrecipes.com/vegan-fried-rice"
  }},
  {{
    "food_name": "Tomato Pasta",
    "recipe": "Boil pasta and mix with tomato sauce.",
    "to_buy": "Basil, olive oil",
    "link": "https://www.allrecipes.com/tomato-pasta"
  }}
]
Do not include any explanations, introductions, or text outside the JSON.
"""}
    ]
  }

  try:
    import anvil.http, json
    response = anvil.http.request(
      "https://api.deepseek.com/chat/completions",
      method="POST",
      headers=headers,
      data=json.dumps(body)
    )

    raw = response.get_bytes().decode()
    data = json.loads(raw)
    message = data["choices"][0]["message"]["content"].strip()
    meals = json.loads(message)
    return meals

  except Exception as e:
    import traceback
    print(traceback.format_exc())
    return [{"food_name": "Error", "recipe": str(e), "to_buy": "", "link": ""}]
