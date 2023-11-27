# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 22:19:44 2023

@author: Oscar Flores

This is the draft that will later become a front end for the optimizer
"""
import streamlit as st
from scipy.optimize import linprog

# Example data
foods = {
    'food1': {'protein': 10, 'carbs': 20, 'fat': 5, 'cost': 2},
    'food2': {'protein': 15, 'carbs': 10, 'fat': 3, 'cost': 3},
    'food3': {'protein': 5, 'carbs': 30, 'fat': 8, 'cost': 1},
}

# Nutritional constraints
nutrient_constraints = {
    'protein': {'min': 30, 'max': 500},
    'carbs': {'min': 40, 'max': 600},
    'fat': {'min': 10, 'max': 200},
}

# Function to calculate the current nutrient amount based on user-defined food quantities
def calculate_current_amount(nutrient):
    min_limit, max_limit = st.session_state.nutrient_limits[nutrient]
    current_value = sum(foods[food][nutrient] * st.session_state.food_quantities.get(food, 0) for food in foods)
    percentage = ((current_value) / (max_limit)) * 100
    return percentage

# Streamlit app
def main():
    st.title("Nutritional Optimization App")

    # Dropdown for selecting a food
    selected_food = st.selectbox("Select a food:", list(foods.keys()))
    
    # Create or get the food_quantities dictionary from session state
    if 'food_quantities' not in st.session_state:
        st.session_state.food_quantities = {}

    # User input for food quantities
    st.session_state.food_quantities[selected_food] = st.slider(f"Quantity of {selected_food}", 0, 100, 0)

    # Display existing sliders
    st.subheader("Current Food Quantities:")
    for food, quantity in st.session_state.food_quantities.items():
        st.write(f"{food}: {quantity}")

#     # Button to optimize
#     if st.button("Optimize"):
#         # Get the user-defined food quantities
#         user_quantities = [food_quantities[food] for food in foods]

#         # Get the user-defined nutrient limits
#         user_limits = [nutrient_limits[nutrient] for nutrient in nutrient_constraints]

#         # Optimize the diet
#         cost, optimized_quantities = optimize_diet(user_quantities, user_limits)

#         # Display results
#         st.subheader("Optimization Results:")
#         st.write(f"Total Cost: {cost:.2f}")
#         st.write("Optimal Food Quantities:")
#         for i, quantity in enumerate(optimized_quantities):
#             st.write(f"{list(foods.keys())[i]}: {quantity}")

# # Function to optimize the diet
# def optimize_diet(user_quantities, user_limits):
#     # Objective function coefficients (costs)
#     c = [foods[food]['cost'] for food in foods]

    # Create or get the nutrient_limits dictionary from session state
    if 'nutrient_limits' not in st.session_state:
        st.session_state.nutrient_limits = {}

    # Sliders for nutrient limits
    st.subheader("Set Nutrient Limits:")
    for nutrient, limits in nutrient_constraints.items():
        st.session_state.nutrient_limits[nutrient] = st.slider(f"Set {nutrient} limit", 0, limits['max'], (limits['min'], limits['max']))

        current_amount = calculate_current_amount(nutrient)
        st.markdown(
            f"""
            <style>
                #progress-container-{nutrient} {{
                    width: 100%;
                    max-width: 100%;
                    overflow: hidden;
                }}
                #progress-container-{nutrient} .stProgressBar div {{
                    background-color: transparent !important;
                    width: 0%;  /* Hide the default progress bar */
                }}
                #progress-container-{nutrient}::before {{
                    content: "";
                    display: block;
                    width: {current_amount}%;  /* Ensure the width is within bounds */
                    height: 10px;
                    background-color: green;
                }}
            </style>
            <div id="progress-container-{nutrient}">
                <div class="stProgressBar">
                    <div style="width: 0%;"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )            


        # # Display a vertical line indicating the current amount for each nutrient
        # st.write(f"Current {nutrient} Amount:")
        # current_amount = sum(foods[food][nutrient] * st.session_state.food_quantities.get(food, 0) for food in foods)
        # st.line_chart({nutrient: [0, current_amount]})



    return None

if __name__ == "__main__":
    main()
    
#%%
# python -m streamlit run C:\Users\52331\Documents\GitHub\NutOpt\streamlit_app.py