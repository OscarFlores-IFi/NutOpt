# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 22:19:44 2023

@author: Oscar Flores

This is the draft that will later become a front end for the optimizer
"""
import streamlit as st
import json
from scipy.optimize import linprog
import numpy as np

directory = r'C:\Users\52331\\'


#%% Define functions

# Function to replace spaces and commas with underscores
def replace_spaces_and_commas_with_underscores(text):
    return text.replace(" ", "_").replace(",", "_")

# Function to replace underscores with spaces
def replace_underscores_with_spaces(text):
    return text.replace("_", " ")

# Function to calculate the current nutrient amount based on user-defined food quantities
def calculate_current_amount(nutrient, foods):
    current_value = sum(foods[food][nutrient] * st.session_state.food_quantities.get(food, 0) for food in foods)
    return round(current_value)

def optimize_food_consumption(foods, selected_foods, nutrient_constraints):
  
    lhs_ineq = []
    rhs_ineq = []
    list_of_foods = []
    
    for nutrient, limits in nutrient_constraints.items():
        not_selected_foods_vector = []
        cont = 0
        for food in foods:
            if food not in st.session_state.food_quantities:
                not_selected_foods_vector.append(foods[food][nutrient]/foods[food]['Calorias']) # We divide by calories to standardize the recipes on a vector of length 1 wrt calories.
                if cont == 0:
                    list_of_foods.append(food)
        
        lhs_ineq.append(not_selected_foods_vector)
        lhs_ineq.append([-i for i in not_selected_foods_vector])
        
        current_amount, _ = calculate_current_amount(nutrient, foods, nutrient_constraints)
        
        rhs_ineq.append(limits['max']-current_amount)
        rhs_ineq.append(current_amount - limits['min'])
        
    # Minimization of objective Function
    obj = np.random.randn(len(lhs_ineq[0]))

    # Boundaries.
    bnd = [(0,700)]*len(lhs_ineq[0])
    
    opt = linprog(c=obj, 
                  A_ub=lhs_ineq, 
                  b_ub=rhs_ineq,
                  bounds=bnd,
                  method = 'highs')
    
    # opt = linprog(c=obj, 
    #               A_ub=lhs_ineq, 
    #               b_ub=rhs_ineq,
    #               bounds=bnd,
    #               method = 'highs',
    #               integrality=1)      
    
    # return ({i:int(j) for i,j in zip(list_of_foods,opt.x) if j >0})
    
    results = {i:np.round(j,2) for i,j in zip(list_of_foods,opt.x) if j > 0}
    
    re_scaled_results = {i:np.round(j/foods[i]['Calorias'],2) for i,j in results.items()}
        
    return (re_scaled_results)

@st.cache_resource
def read_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

#%% Read files

# Food nutritional facts
foods = read_json(directory + "avena_food_nutrients.json")
    
"avena_food_categories.json"

# Nutritional constraints
nutrient_constraints = read_json(directory + "avena_nutrition_constraints.json")

    
list_of_ingredients = read_json(directory + "avena_ingredient_list.json")

# with open("avena_ingredient_list1.json", "w") as file:
#     json.dump(list_of_ingredients, file)
#%% Streamlit app
def main():
    st.title("Nutritional Optimization App")


    if st.button("Reset"):
        del st.session_state.food_quantities
        # Delete all the items in Session state
        for key in st.session_state.keys():
            del st.session_state[key]

    # Dropdown for selecting a food
    selected_food = st.selectbox("Selecciona una comida:", list(foods.keys()))
    
    # Create or get the food_quantities dictionary from session state
    if 'food_quantities' not in st.session_state:
        st.session_state.food_quantities = {}

    # User input for food quantities
    if selected_food in st.session_state.food_quantities:        
        st.session_state.food_quantities[selected_food] = st.slider(f"Cantidad de {selected_food}", 0.0, 5.0, float(st.session_state.food_quantities[selected_food]))
    else:
        st.session_state.food_quantities[selected_food] = st.slider(f"Cantidad de {selected_food}", 0.0, 5.0, 0.0)

    # Button to optimize
    if st.button("Optimize"):
        try:
            new_items = optimize_food_consumption(foods, st.session_state.food_quantities, nutrient_constraints)

            for new_food, new_quantity in new_items.items(): 
                st.session_state.food_quantities[new_food] = new_quantity
        except:
            st.write(":blue[Optimizacion no es posible. Por favor ajusta la seleccion]")
            


    # Display existing sliders
    st.subheader("Cantidades actuales:")
    for food, quantity in st.session_state.food_quantities.items():
        st.write(f"https:/avena.io{food}: {quantity}")

    # Create or get the nutrient_limits dictionary from session state
    if 'nutrient_limits' not in st.session_state:
        st.session_state.nutrient_limits = {}

    # Sliders for nutrient limits
    st.subheader("Limites nutricionales:")
    for nutrient, limits in nutrient_constraints.items():
        identifier = replace_spaces_and_commas_with_underscores(nutrient)
        st.session_state.nutrient_limits[identifier] = st.slider(f"Limite de {nutrient}",                          \
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
# python -m streamlit run C:\Users\52331\Documents\GitHub\NutOpt\streamlit_app_avena.py