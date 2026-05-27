from pydantic import BaseModel, Field
from typing import List

class MacroBreakdown(BaseModel):
    calories: int = Field(description="Total estimated calories for the recipe")
    protein: int = Field(description="Protein in grams")
    carbohydrates: int = Field(description="Carbohydrates in grams")
    fats: int = Field(description="Fats in grams")

class RecipeResponse(BaseModel):
    recipe_name: str = Field(description="A creative name for the recipe")
    cooking_time: str = Field(description="Estimated preparation and cooking time")

    # TODO: Add a field for the list of required ingredients
    required_ingredients: List[str] = Field(description="The required ingredients for the dish")

    # TODO: Add a field for the step-by-step instructions
    instructions: List[str] = Field(description="Step-by-step instructions to cook the dish")

    macros: MacroBreakdown
    shopping_list: List[str] = Field(description="Ingredients needed for the recipe that were NOT in the user's input")