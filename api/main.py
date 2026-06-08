import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types
from sqlalchemy.orm import Session
from api.schemas import RecipeResponse, MacroBreakdown
from api.database import get_db
from api.models import RecipeDB

app = FastAPI()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins to talk to your backend
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, OPTIONS, etc.
    allow_headers=["*"],  # Allows any custom headers (like Auth tokens)
)

@app.post("/api/generate-recipe", response_model=RecipeResponse)
async def generate_recipe(ingredients: list[str], db: Session = Depends(get_db)):
    try:
        ingredients_string = ", ".join(ingredients)
        prompt = f"You are an expert chef. Create a recipe using these ingredients: {ingredients_string}. Highlight any missing items."

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=RecipeResponse,
                temperature=0.7
            ),
        )

        recipe_data = RecipeResponse.model_validate_json(response.text)

        new_recipe = RecipeDB(
            recipe_name=recipe_data.recipe_name,
            cooking_time=recipe_data.cooking_time,
            required_ingredients=recipe_data.required_ingredients,
            instructions=recipe_data.instructions,
            macros=recipe_data.macros.model_dump(),
            shopping_list=recipe_data.shopping_list
        )


        db.add(new_recipe)
        db.commit()
        db.refresh(new_recipe)

        return recipe_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))