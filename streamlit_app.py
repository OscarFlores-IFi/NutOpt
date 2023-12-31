# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 22:19:44 2023

@author: Oscar Flores

This is the draft that will later become a front end for the optimizer
"""
import streamlit as st
import json
from scipy.optimize import linprog

directory = r'C:\Users\52331\Documents\GitHub\NutOpt\\'


#%% Define functions

# Function to replace spaces and commas with underscores
def replace_spaces_and_commas_with_underscores(text):
    return text.replace(" ", "_").replace(",", "_")

# Function to replace underscores with spaces
def replace_underscores_with_spaces(text):
    return text.replace("_", " ")

# Function to calculate the current nutrient amount based on user-defined food quantities
def calculate_current_amount(nutrient, foods, nutrient_constraints):
    current_value = sum(foods[food][nutrient] * st.session_state.food_quantities.get(food, 0) for food in foods)
    percentage = (current_value / (nutrient_constraints[nutrient]['max']*1.3))
    if percentage < 1:
        return (round(current_value), percentage)
    return (round(current_value), 100)


def get_text_to_show(identifier, current_amount):
    min_limit, max_limit = st.session_state.nutrient_limits[identifier]
    if current_amount < min_limit:
        return ":orange[below limits]"  
    elif current_amount > max_limit:
        return ":orange[above limits]"      
    else:
        return ":green[within limits]"

def optimize_food_consumption(foods, selected_foods, nutrient_constraints):
  
    lhs_ineq = []
    rhs_ineq = []
    list_of_foods = []
    
    for nutrient, limits in nutrient_constraints.items():
        not_selected_foods_vector = []
        cont = 0
        for food in foods:
            if food not in st.session_state.food_quantities:
                not_selected_foods_vector.append(foods[food][nutrient])
                if cont == 0:
                    list_of_foods.append(food)
        
        lhs_ineq.append(not_selected_foods_vector)
        lhs_ineq.append([-i for i in not_selected_foods_vector])
        
        current_amount, _ = calculate_current_amount(nutrient, foods, nutrient_constraints)
        
        rhs_ineq.append(limits['max']-current_amount)
        rhs_ineq.append(current_amount - limits['min'])
        
    # Minimization of objective Function
    obj = [-1]* len(lhs_ineq[0])

    # Boundaries. Maximum 300 grams of any given product per day.
    bnd = [(0,200)]*len(lhs_ineq[0])
    
    opt = linprog(c=obj, 
                  A_ub=lhs_ineq, 
                  b_ub=rhs_ineq,
                  bounds=bnd,
                  method = 'highs',
                  integrality=1)
        
    return ({i:int(j) for i,j in zip(list_of_foods,opt.x) if j >0})

@st.cache_resource
def read_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

#%% Read files

# Food nutritional facts
foods = read_json(directory + "food_nutrients.json")
    
# Nutritional constraints
nutrient_constraints = read_json(directory + "nutrition_constraints.json")
print(nutrient_constraints)

    
#%% Streamlit app
def main():
    st.title("Nutritional Optimization App")


    if st.button("Reset"):
        del st.session_state.food_quantities
        # Delete all the items in Session state
        for key in st.session_state.keys():
            del st.session_state[key]

    # Dropdown for selecting a food
    selected_food = st.selectbox("Select a food:", list(foods.keys()))
    
    # Create or get the food_quantities dictionary from session state
    if 'food_quantities' not in st.session_state:
        st.session_state.food_quantities = {}

    # User input for food quantities
    if selected_food in st.session_state.food_quantities:        
        st.session_state.food_quantities[selected_food] = st.slider(f"Quantity of {selected_food} (g)", 0, 400, st.session_state.food_quantities[selected_food])
    else:
        st.session_state.food_quantities[selected_food] = st.slider(f"Quantity of {selected_food} (g)", 0, 400, 0)

    # Button to optimize
    if st.button("Optimize"):
        try:
            new_items = optimize_food_consumption(foods, st.session_state.food_quantities, nutrient_constraints)

            for new_food, new_quantity in new_items.items(): 
                st.session_state.food_quantities[new_food] = new_quantity
        except:
            st.write(":blue[Optimization not possible, please make sure all items are below boundaries.]")
            


    # Display existing sliders
    st.subheader("Current Food Quantities:")
    for food, quantity in st.session_state.food_quantities.items():
        st.write(f"{food}: {quantity}")

    # Create or get the nutrient_limits dictionary from session state
    if 'nutrient_limits' not in st.session_state:
        st.session_state.nutrient_limits = {}

    # Sliders for nutrient limits
    st.subheader("Nutrient Limits:")
    for nutrient, limits in nutrient_constraints.items():
        identifier = replace_spaces_and_commas_with_underscores(nutrient)
        st.session_state.nutrient_limits[identifier] = st.slider(f"{nutrient} limits",                          \
                                                                 0,                                             \
                                                                 int(limits['max']*1.3),                        \
                                                                 (int(limits['min']), int(limits['max'])))
   
        current_amount, percentage_of_max_lim = calculate_current_amount(nutrient, foods, nutrient_constraints)
        text_to_show = get_text_to_show(identifier, current_amount)
        
        # Use st.progress for the progress bar
        st.progress(percentage_of_max_lim, text=text_to_show)    


    for nutrient, limits in nutrient_constraints.items():
        current_amount, _ = calculate_current_amount(nutrient, foods, nutrient_constraints)
        st.write(f"{nutrient}: {current_amount}")

if __name__ == "__main__":
    main()
    
#%%
# python -m streamlit run C:\Users\52331\Documents\GitHub\NutOpt\streamlit_app.py