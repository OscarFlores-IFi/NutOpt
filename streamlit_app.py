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
    percentage = ((current_value - min_limit) / (max_limit - min_limit)) * 100
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
        st.session_state.nutrient_limits[nutrient] = st.slider(f"Set {nutrient} limit", limits['min'], limits['max'], (limits['min'], limits['max']))


        # Display a green line above the slider indicating the current amount for each nutrient
        current_amount = calculate_current_amount(nutrient)
        st.markdown(
             f"""
             <style>
                 #slider-container-{nutrient} {{
                     position: relative;
                 }}
                 #slider-container-{nutrient}::before {{
                     content: "";
                     position: absolute;
                     top: 0;
                     left: 0;
                     width: {current_amount}%;
                     height: 100%;
                     background-color: green;
                     z-index: 1;
                 }}
             </style>
             <div id="slider-container-{nutrient}">
                 {st.slider(f"Slider for {nutrient}", 0, 100, 0, key=f"{nutrient}_slider")}
             </div>
             """,
             unsafe_allow_html=True
         )                            
                                                
    # Display existing nutrient limits
    st.subheader("Current Nutrient Limits:")
    for nutrient, limits in st.session_state.nutrient_limits.items():
        st.write(f"{nutrient}: {limits[0]} to {limits[1]}")
                                            
           
    # Display the sum of product * nutrient for each nutrient
    for nutrient in nutrient_constraints:
        st.subheader(f"Sum of {selected_food}'s {nutrient} Contribution:")
        sum_product = calculate_current_amount(nutrient)
        st.write(f"{sum_product:.2f}")


        # # Display a vertical line indicating the current amount for each nutrient
        # st.write(f"Current {nutrient} Amount:")
        # current_amount = sum(foods[food][nutrient] * st.session_state.food_quantities.get(food, 0) for food in foods)
        # st.line_chart({nutrient: [0, current_amount]})



    return None

if __name__ == "__main__":
    main()
    
#%%
# python -m streamlit run C:\Users\52331\Documents\GitHub\NutOpt\streamlit_app.py