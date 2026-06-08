import streamlit as st
import json
from google import genai
from google.genai import types

st.set_page_config(page_title="Fridget AI Chef", page_icon="🍳", layout="centered")

st.title("🍳 Fridget AI Chef")
st.subheader("Raid your fridge and let AI cook up the perfect meal!")

# --- SECURE API KEY INITIALIZATION ---
# This looks for an environment variable or a Streamlit Secret
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    # Fallback for local development if you haven't set up secrets yet
    api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

# Initialize the Gemini Client
if api_key:
    client = genai.Client(api_key=api_key)
else:
    st.warning("Please provide a Gemini API Key to proceed.")
    st.stop()

# --- STATE MANAGEMENT ---
if "ingredients_list" not in st.session_state:
    st.session_state.ingredients_list = []

# --- INGREDIENT INPUT FORM ---
with st.form(key="ingredient_form", clear_on_submit=True):
    new_ingredient = st.text_input("Type an ingredient and press Enter:", placeholder="e.g., eggs, bacon, cheese")
    submit_button = st.form_submit_button(label="➕ Add Ingredient")

if submit_button and new_ingredient:
    clean_item = new_ingredient.strip().lower()
    if clean_item and clean_item not in st.session_state.ingredients_list:
        st.session_state.ingredients_list.append(clean_item)
        st.rerun()

# --- DISPLAY CURRENT INGREDIENTS ---
if st.session_state.ingredients_list:
    st.write("### Your Current Ingredients:")
    st.info(", ".join(st.session_state.ingredients_list))

    if st.button("🗑️ Clear Ingredients"):
        st.session_state.ingredients_list = []
        st.rerun()

    st.markdown("---")

# --- NATIVE AI RECIPE GENERATION ---
if st.session_state.ingredients_list:
    if st.button("🚀 Raid the Fridge!", type="primary"):
        with st.spinner("Chef Gemini is cooking up a recipe... (No time limits!)"):
            try:
                # Define exactly what JSON structure we want Gemini to return
                recipe_schema = types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "recipe_name": types.Schema(type=types.Type.STRING),
                        "cooking_time": types.Schema(type=types.Type.STRING),
                        "macros": types.Schema(
                            type=types.Type.OBJECT,
                            properties={
                                "calories": types.Schema(type=types.Type.STRING),
                                "protein": types.Schema(type=types.Type.STRING),
                                "carbohydrates": types.Schema(type=types.Type.STRING),
                            }
                        ),
                        "instructions": types.Schema(
                            type=types.Type.ARRAY,
                            items=types.Schema(type=types.Type.STRING)
                        )
                    },
                    required=["recipe_name", "cooking_time", "macros", "instructions"]
                )

                prompt = f"Create a wonderful recipe using some or all of these ingredients: {', '.join(st.session_state.ingredients_list)}. Be concise with instructions."

                # Call Gemini directly!
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=recipe_schema,
                        temperature=0.7
                    ),
                )

                # Convert the response text straight into a Python dictionary
                recipe_data = json.loads(response.text)

                # --- DISPLAY RESULTS ---
                st.success(f"## {recipe_data.get('recipe_name')}")
                st.write(f"⏱️ **Cooking Time:** {recipe_data.get('cooking_time')}")

                col1, col2, col3 = st.columns(3)
                macros = recipe_data.get('macros', {})
                col1.metric("Calories", macros.get('calories', 'N/A'))
                col2.metric("Protein", macros.get('protein', 'N/A'))
                col3.metric("Carbs", macros.get('carbohydrates', 'N/A'))

                st.write("### 📝 Instructions:")
                for step in recipe_data.get('instructions', []):
                    st.write(f"- {step}")

            except Exception as e:
                st.error(f"Error generating recipe: {str(e)}")