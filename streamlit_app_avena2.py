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

directory = r"C:\Users\52331\Documents\GitHub\NutOpt\\"


#%% Define functions

# Function to replace spaces and commas with underscores
def replace_spaces_and_commas_with_underscores(text):
    return text.replace(" ", "_").replace(",", "_")

# Function to replace underscores with spaces
def replace_underscores_with_spaces(text):
    return text.replace("_", " ")

# # Function to calculate the current category amount based on user-defined food quantities
# def calculate_current_amount_categories(category, food_categories):
#     current_value = sum(food_categories[food][category] * st.session_state.food_quantities.get(food, 0) for food in food_categories)
#     return (current_value)

# Function to calculate the current category amount based on user-defined food quantities
def calculate_current_amount(category, foods):
    current_value = sum(foods[food][category] * st.session_state.food_quantities.get(food, 0) for food in foods)

    percentage = (current_value / (10))
    if percentage < 1:
        return (round(current_value), percentage)
    return (round(current_value), 100)


def get_text_to_show(identifier, current_amount):
    min_limit, max_limit = st.session_state.category_limits[identifier]
    if current_amount < min_limit:
        return ":orange[below limits]"  
    elif current_amount > max_limit:
        return ":orange[above limits]"      
    else:
        return ":green[within limits]"

def optimize_food_consumption(food_categories, selected_foods, category_constraints):
  
    lhs_ineq = []
    rhs_ineq = []
    list_of_foods = []
    
    cont = 0
    
    for category, limits in category_constraints.items():
        not_selected_foods_vector = []
        for food in food_categories:
            if food not in st.session_state.food_quantities:
                not_selected_foods_vector.append(food_categories[food][category]) 
                if cont == 0:
                    list_of_foods.append(food)
        cont += 1
        
        lhs_ineq.append(not_selected_foods_vector)
        lhs_ineq.append([-i for i in not_selected_foods_vector])
        
        current_amount_category , _ = calculate_current_amount(category, food_categories)
        
        identifier = replace_spaces_and_commas_with_underscores(category)
        min_, max_ = st.session_state.category_limits[identifier]
        
        rhs_ineq.append(max_-current_amount_category)
        rhs_ineq.append(current_amount_category - min_)
        
    # Minimization of objective Function
    obj = np.random.randn(len(lhs_ineq[0]))

    # Boundaries.
    bnd = [(0,10)]*len(lhs_ineq[0]) # set boundaries for each of the foods between (a,b)
    
    # opt = linprog(c=obj, 
    #               A_ub=lhs_ineq, 
    #               b_ub=rhs_ineq,
    #               bounds=bnd,
    #               method = 'highs')
    
    # return ({i:np.round(j,2) for i,j in zip(list_of_foods,opt.x) if j > 0})

    opt = linprog(c=obj, 
                  A_ub=lhs_ineq, 
                  b_ub=rhs_ineq,
                  bounds=bnd,
                  method = 'highs',
                  integrality=1)      
      
    return ({i:round(j) for i,j in zip(list_of_foods,opt.x) if j >0})
    
@st.cache_resource
def read_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

#%% Read files
# Food nutritional facts
food_nutrients = read_json(directory + "avena_food_nutrients.json")
# Nutritional constraints
category_constraints = read_json(directory + "category_constraints.json")
category_names = {"1": "Verduras",
                     "2": "Frutas",
                     "3": "Cereales sin grasa",
                     "4": "Cereales con grasa",
                     "5": "Leguminosas",
                     "6": "Proteinas muy bajas en Grasa",
                     "7": "Proteinas bajas en Grasa",
                     "8": "Proteinas moderadas en Grasa",
                     "9": "Proteinas altas en Grasa",
                     "10": "Leche deslactosada",
                     "11": "Leche semideslactosada",
                     "12": "Leche entera",
                     "13": "Leche con azucar",
                     "14": "Grasas sin Proteina",
                     "15": "Grasas con Proteina"}
# Food categories
food_categories = read_json(directory + "avena_food_categories.json")

#%% Streamlit app
def main():
                    
    # np.random.seed(123)
    st.title("Nutritional Optimization App")

    list_of_food_nutrients = food_nutrients[list(food_nutrients)[0]].keys()

    if st.button("Reset"):
        del st.session_state.food_quantities
        # Delete all the items in Session state
        for key in st.session_state.keys():
            del st.session_state[key]

    # Dropdown for selecting a food
    selected_food = st.selectbox("Selecciona una comida:", list(food_categories.keys()))
    
    # Create or get the food_quantities dictionary from session state
    if 'food_quantities' not in st.session_state:
        st.session_state.food_quantities = {}

    # User input for food quantities
    if selected_food in st.session_state.food_quantities:        
        st.session_state.food_quantities[selected_food] = st.slider(f"Cantidad de {selected_food}", 0, 10, int(st.session_state.food_quantities[selected_food]))
    else:
        st.session_state.food_quantities[selected_food] = st.slider(f"Cantidad de {selected_food}", 0, 10, 0)

    # Button to optimize
    if st.button("Optimize"):
        try:
            new_items = optimize_food_consumption(food_categories, st.session_state.food_quantities, category_constraints)
            for new_food, new_quantity in new_items.items(): 
                st.session_state.food_quantities[new_food] = new_quantity
        except:
            st.write(":blue[Optimizacion no es posible. Por favor ajusta la seleccion]")
            
            
    # Display existing sliders
    st.subheader("Cantidades actuales:")
    for food, quantity in st.session_state.food_quantities.items():
        st.write(f"https:/avena.io{food}: {int(quantity)}")

    # Create or get the category_limits dictionary from session state
    if 'category_limits' not in st.session_state:
        st.session_state.category_limits = {}

    # Sliders for category limits
    st.subheader("Limites nutricionales:")
    for category, limits in category_constraints.items():
        identifier = replace_spaces_and_commas_with_underscores(category)
        st.session_state.category_limits[identifier] = st.slider(f"Limite de {category_names[category]}",                          \
                                                                 0,                                             \
                                                                 10,                        \
                                                                 (int(limits['min']), int(limits['max'])))
   
        current_amount, percentage_of_max_lim = calculate_current_amount(category, food_categories)
        text_to_show = get_text_to_show(identifier, current_amount)
        
        # Use st.progress for the progress bar
        st.progress(percentage_of_max_lim, text=text_to_show)    

    for nutrient in list_of_food_nutrients:
        current_amount, _ = calculate_current_amount(nutrient, food_nutrients)
        st.write(f"{nutrient}: {current_amount}")    

if __name__ == "__main__":
    main()
    
#%%
# python -m streamlit run C:\Users\52331\Documents\GitHub\NutOpt\streamlit_app_avena2.py