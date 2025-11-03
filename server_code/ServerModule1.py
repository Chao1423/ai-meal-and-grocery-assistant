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
def suggest_meals(ingredients):
  """Call DeepSeek to get meals, recipes, and extra ingredients as JSON."""
  row = app_tables.config.get(name='DEEPSEEK_API_KEY')
  if not row:
    return [{"food_name": "Error", "recipe": "Missing API key", "to_buy": ""}]
  api_key = row['value']

  headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
  }

  # ✅ Tell the model to respond in a *strict JSON list* format
  body = {
    "model": "deepseek-chat",
    "max_tokens": 400,
    "messages": [
      {"role": "system", "content": "You are a helpful cooking assistant."},
      {"role": "user", "content": f"""
I currently have these ingredients: {ingredients}.
Return your answer **strictly as a JSON list** of objects, each with keys:
- food_name
- recipe
- to_buy
Example:
[
  {{"food_name": "Fried Rice", "recipe": "Cook rice with egg and soy sauce", "to_buy": "Green peas"}},
  {{"food_name": "Tomato Omelette", "recipe": "Mix tomato with egg", "to_buy": "Cheese"}}
]
Do not include any extra text.
"""}
    ]
  }

  try:
    response = anvil.http.request(
      "https://api.deepseek.com/chat/completions",
      method="POST",
      headers=headers,
      data=json.dumps(body)
    )

    raw = response.get_bytes().decode()
    data = json.loads(raw)

    # The model's content string
    message = data["choices"][0]["message"]["content"].strip()

    # Parse the JSON inside the model's output
    meals = json.loads(message)
    return meals

  except Exception as e:
    import traceback
    print(traceback.format_exc())
    return [{"food_name": "Error", "recipe": str(e), "to_buy": ""}]

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
# 
