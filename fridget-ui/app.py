import streamlit as st
import requests

st.set_page_config(page_title="Fridget AI Chef", page_icon="🍳", layout="centered")

st.title("🍳 Fridget AI Chef")
st.subheader("Raid your fridge and let AI cook up the perfect meal!")

# Initialize session state
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

    st.markdown("---")  # Visual separator

# --- API CALL SECTION ---
if st.session_state.ingredients_list:
    if st.button("🚀 Raid the Fridge!", type="primary"):
        with st.spinner("Chef Gemini is cooking up a recipe..."):
            try:
                url = "https://fridget-ai.vercel.app/api/generate-recipe"
                payload = {"ingredients": st.session_state.ingredients_list}

                response = requests.post(url, json=payload)

                if response.status_code == 200:
                    recipe_data = response.json()

                    st.success(f"## {recipe_data.get('recipe_name', 'Your Custom Recipe')}")
                    st.write(f"⏱️ **Cooking Time:** {recipe_data.get('cooking_time', 'N/A')}")

                    col1, col2, col3 = st.columns(3)
                    macros = recipe_data.get('macros', {})
                    col1.metric("Calories", macros.get('calories', 'N/A'))
                    col2.metric("Protein", macros.get('protein', 'N/A'))
                    col3.metric("Carbs", macros.get('carbohydrates', 'N/A'))

                    st.write("### 📝 Instructions:")
                    for step in recipe_data.get('instructions', []):
                        st.write(f"- {step}")
                else:
                    st.error(f"Backend returned an error: {response.status_code}")

            except Exception as e:
                st.error(f"Could not connect to backend: {str(e)}")