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
    """Call the AI and populate the DataGrid."""
    ingredients = self.ingredients_box.text.strip()
    if not ingredients:
      alert("Please enter your available ingredients first!")
      return

    # ✅ Hide the whole grid while loading
    self.data_grid_1.visible = False
    Notification("Generating meal ideas... please wait ⏳").show()

    try:
      meals = anvil.server.call('suggest_meals', ingredients)
      print("DEBUG meals:", meals)  # debug log

      if isinstance(meals, list):
        # ✅ Set items on the RepeatingPanel (the inner component)
        self.data_grid_meals.items = meals

        # ✅ Show the DataGrid after filling data
        self.data_grid_1.visible = True

        Notification(f"✅ Generated {len(meals)} meal ideas!").show()
      else:
        alert("The AI returned an unexpected format.")
    except Exception as e:
      alert(f"Error: {e}")

  def ingredients_box_pressed_enter(self, **event_args):
    """Called when the user presses Enter in the text box"""
    self.generate_meal_suggestions()

  def button_1_click(self, **event_args):
    """Triggered when the user clicks the Generate Suggestions button"""
    self.generate_meal_suggestions()



