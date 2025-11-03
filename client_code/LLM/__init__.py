from ._anvil_designer import LLMTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server

class LLM(LLMTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  def generate_button_click(self, **event_args):
    """Triggered when the user clicks 'Generate Suggestions'"""
    ingredients = self.ingredients_box.text.strip()
    if not ingredients:
      self.output_area.text = "Please enter your available ingredients first!"
      return

    self.output_area.text = "Generating meal ideas... please wait."

    try:
      result = anvil.server.call('suggest_meals', ingredients)
      self.output_area.text = result
    except Exception as e:
      self.output_area.text = f"An error occurred: {e}"
