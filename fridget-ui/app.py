import streamlit as st
import requests

st.set_page_config(page_title="Fridget AI Chef", page_icon="🍳", layout="centered")

st.title("🍳 Fridget AI Chef")
st.subheader("Raid your fridge and let AI cook up the perfect meal!")

if "ingredients_list" not in st.session_state:
    st.session_state.ingredients_list = []

new_ingredient = st.text_input("Type an ingredient and press Enter:", placeholder="e.g., eggs, bacon, cheese")

if new_ingredient:
    clean_item = new_ingredient.strip().lower()
    if clean_item and clean_item not in st.session_state.ingredients_list:
        st.session_state.ingredients_list.append(clean_item)

    st.rerun()

if st.session_state.ingredients_list:
    st.write("### Your Current Basket:")
    st.info(", ".join(st.session_state.ingredients_list))

if st.button("Clear Basket"):
    st.session_state.ingredients_list = []
    st.rerun()

if st.session_state.ingredients_list:
    if st.button("🚀 Raid the Fridge!", type="primary"):

        with st.spinner("Chef Gemini is cooking up a recipe..."):
            try:

                url = "https://fridget-ai.vercel.app/api/generate-recipe"

                payload = {
                    "ingredients": st.session_state.ingredients_list
                }

                response = requests.post(url, json=payload)

                if response.status_code == 200:
                    recipe_data = response.json()

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
                else:
                    st.error(f"Backend returned an error: {response.status_code}")

            except Exception as e:
                st.error(f"Could not connect to backend: {str(e)}")