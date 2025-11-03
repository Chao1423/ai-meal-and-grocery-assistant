from ._anvil_designer import LLMTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
import json

class LLM(LLMTemplate):
  def __init__(self, **properties):
    # Initialize UI components
    self.init_components(**properties)
    
  def text_box_1_pressed_enter(self, **event_args):
    """Called when the user presses Enter in the TextBox"""
    self.generate_meal_suggestions()

  def generate_meal_suggestions(self):
    """Shared logic: call the server function and update the output area"""
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

  def ingredients_box_pressed_enter(self, **event_args):
    """Called when the user presses Enter in the text box"""
    self.generate_meal_suggestions()

  def button_1_click(self, **event_args):
    """Triggered when the user clicks the Generate Suggestions button"""
    self.generate_meal_suggestions()

def drop_down_1_change(self, **event_args):
  """This method is called when an item is selected"""
  selected = self.ingredients_dropdown.selected_value
  if not selected:
    self.output_area.text = "Please select an ingredient."
    return

  self.output_area.text = f"You selected: {selected}\nGenerating ideas..."

  try:
    result = anvil.server.call('suggest_meals', selected)
    # Expecting DeepSeek to return structured JSON text
    try:
      data = json.loads(result)  # in case AI returns a JSON array
    except:
      data = self.parse_ai_text(result)  # fallback parser below

    self.display_table(data)
  except Exception as e:
    self.output_area.text = f"Error: {e}"

