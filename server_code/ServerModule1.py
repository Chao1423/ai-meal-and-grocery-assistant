import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.http
import json

import anvil.server
import anvil.http
from anvil.tables import app_tables
import json

@anvil.server.callable
def suggest_meals(ingredients):
  row = app_tables.config.get(name='DEEPSEEK_API_KEY')
  if not row:
    return "Error: No API key found in the 'config' table."
  api_key = row['value']

  headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
  }

  # ✅ correct DeepSeek JSON payload
  body = {
    "model": "deepseek-chat",
    "max_tokens": 300,      
    "messages": [
      {"role": "system", "content": "You are a helpful cooking assistant."},
      {"role": "user", "content": f"I have these ingredients: {ingredients}. Suggest meals and what else to buy."}
    ]
  }

  try:
    # 👇 serialize body explicitly to ensure valid JSON
    response = anvil.http.request(
      "https://api.deepseek.com/chat/completions",
      method="POST",
      headers=headers,
      data=json.dumps(body)  # ✅ instead of `json=body`
    )

    raw = response.get_bytes().decode()
    print("Raw API response:\n", raw)

    data = json.loads(raw)
    return data["choices"][0]["message"]["content"]

  except anvil.http.HttpError as e:
    # decode and show readable content if possible
    try:
      err_msg = e.response.get_bytes().decode()
    except:
      err_msg = str(e)
    return f"HTTP Error {e.status}: {err_msg}"

  except Exception as e:
    import traceback
    print(traceback.format_exc())
    return f"Unexpected error: {e}"


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
