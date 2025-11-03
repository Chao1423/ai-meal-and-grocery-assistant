import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.http

@anvil.server.callable
def suggest_meals(ingredients):
  """
    Given a list of available ingredients,
    call DeepSeek API to generate meal ideas and shopping suggestions.
    """
  # Retrieve API key from your Data Table
  api_key = app_tables.config.get(name='DEEPSEEK_API_KEY')['value']

  headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
  }

  body = {
    "model": "deepseek-chat",
    "messages": [
      {"role": "system", "content": "You are a helpful cooking assistant."},
      {"role": "user", "content": f"""
I currently have these ingredients: {ingredients}.
1. List some meals I can make with them.
2. Suggest additional ingredients I could buy to make more interesting dishes.
3. Recommend new recipes combining both existing and suggested ingredients.
Please format your answer clearly using numbered lists.
            """}
    ]
  }

  response = anvil.http.request(
    "POST",
    "https://api.deepseek.com/chat/completions",
    headers=headers,
    json=body
  )

  # Return the AI's response text
  return response['choices'][0]['message']['content']

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
