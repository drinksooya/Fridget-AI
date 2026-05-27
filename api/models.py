from sqlalchemy import Column, Integer, String, JSON
# Import the Base class from your database setup file
from .database import Base


class RecipeDB(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    recipe_name = Column(String, nullable=False)
    cooking_time = Column(String, nullable=True)

    required_ingredients = Column(JSON, nullable=False)
    instructions = Column(JSON, nullable=False)
    macros = Column(JSON, nullable=False)
    shopping_list = Column(JSON, nullable=False)