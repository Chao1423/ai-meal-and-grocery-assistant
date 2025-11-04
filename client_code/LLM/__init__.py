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
    self.image_1.style = {
      "filter": "brightness(1.1) drop-shadow(0 0 8px rgba(0, 0, 0, 0.1))"
    }

  def text_box_1_pressed_enter(self, **event_args):
    """Called when the user presses Enter in the TextBox"""
    self.generate_meal_suggestions()

  def generate_meal_suggestions(self):
    """Call the AI and populate the DataGrid."""
    ingredients = self.ingredients_box.text.strip()
    allergies = self.allergies_box.text.strip()
    vegan_pref = self.vegan_check.checked

    if not ingredients:
      alert("Please enter your available ingredients first!")
      return

    self.data_grid_1.visible = False
    Notification("Generating meal ideas... please wait ⏳").show()


    try:
      # ✅ Pass new parameters to the server
      meals = anvil.server.call('suggest_meals', ingredients, allergies, vegan_pref)
      print("DEBUG meals:", meals)

      if isinstance(meals, list):   
        self.data_grid_meals.items = meals
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



