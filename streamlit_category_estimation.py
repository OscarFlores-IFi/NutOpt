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

# # Function to calculate the current category amount based on user-defined food quantities
# def calculate_current_amount_categories(category, food_categories):
#     current_value = sum(food_categories[food][category] * st.session_state.food_quantities.get(food, 0) for food in food_categories)
#     return (current_value)

# Function to calculate the current category amount based on user-defined food quantities
def calculate_current_macros(macronutrient):
    multiplier = {'Proteinas': 4, 'Lipidos': 9, 'Carbohidratos': 4}

    current_macro = sum(st.session_state.smae_categories.get(category, 0) *  \
                    smae_categories[replace_underscores_with_spaces(category)].get(macronutrient)  \
                    for category in st.session_state.smae_categories.keys())
        
    current_energy_per_macro = sum(multiplier[macronutrient] *  \
                    st.session_state.smae_categories.get(category, 0) *  \
                    smae_categories[replace_underscores_with_spaces(category)].get(macronutrient)  \
                    for category in st.session_state.smae_categories.keys())

    
    return round(current_macro), round(current_energy_per_macro) 


def get_text_color(maximum, category):
    
    current_amount = st.session_state.smae_categories.get(replace_spaces_and_commas_with_underscores(category), 0)
    if current_amount > maximum:
        return f":orange[{category}, Current:{current_amount}, Max:{maximum})]"
    elif current_amount == maximum:
        return f":white[{category}, Current:{current_amount}, Max:{maximum})]"
    else:
        return f":green[{category}, Current:{current_amount}, Max:{maximum})]"

def calculate_max(category, identifier, limits):
    
    multiplier = {'Proteinas': 4, 'Lipidos': 9, 'Carbohidratos': 4}

    lhs_ineq = []
    rhs_ineq = []
       
    for macronutrient in limits:
        list_of_categories = []
        
        for cat in smae_categories:
            list_of_categories.append(smae_categories[cat][macronutrient] * multiplier[macronutrient]) 
        
        lhs_ineq.append(list_of_categories)
        lhs_ineq.append([-i for i in list_of_categories])
        
        _, current_energy_per_macro = calculate_current_macros(macronutrient)
        
        min_ = limits[macronutrient]['min']
        max_ = limits[macronutrient]['max']
        
        rhs_ineq.append(max_ - current_energy_per_macro)
        rhs_ineq.append(current_energy_per_macro - min_)
                
    # Boundaries.
    bnd = [(0,100)]*len(lhs_ineq[0]) # set boundaries for each of the foods between (a,b)

    #################    
    # FOR THE MAXIMUM:
    # Minimization of objective Function
    obj = np.zeros(len(smae_categories))
    idx = list(smae_categories.keys()).index(category)
    obj[idx] = -1

    opt = linprog(c=obj, 
                  A_ub=lhs_ineq, 
                  b_ub=rhs_ineq,
                  bounds=bnd,
                  method = 'highs')
    
    # return ({i:np.round(j,2) for i,j in zip(list_of_foods,opt.x) if j > 0})

    # opt = linprog(c=obj, 
    #               A_ub=lhs_ineq, 
    #               b_ub=rhs_ineq,
    #               bounds=bnd,
    #               method = 'highs',
    #               integrality=1)      
    try: 
        maximum = np.floor(opt.x[idx]) + st.session_state.smae_categories.get(identifier, 0)
    except:
        maximum = 0
    
    return(maximum)

    # return ({i:round(j) for i,j in zip(list_of_foods,opt.x) if j >0})
    
@st.cache_resource
def read_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

#%% Read files
# Food categories
smae_categories = read_json(directory + "smae_equivalents.json")

#%% Streamlit app
def main():
                     
    st.title("Nutritional Optimization App")
    
    # Calories = st.text_input('Calorie consumption:', 2000)
    Calories = 2200

    limits = {"Proteinas":{"min":Calories*0.1,"max":Calories*0.35}, 
              "Lipidos":{"min":Calories*0.2,"max":Calories*0.35}, 
              "Carbohidratos":{"min":Calories*0.45,"max":Calories*0.65}}
    
    # if st.button("Reset"):
    #     # Delete all the items in Session state
    #     for key in smae_categories.keys():
    #         try:
    #             del st.session_state.smae_categories[key]
    #         except KeyError:
    #             pass
    #     del st.session_state.smae_categories


    # Dropdown for selecting a food
    # selected_food = st.selectbox("Selecciona una comida:", list(food_categories.keys()))
    
    # # Create or get the food_quantities dictionary from session state
    if 'smae_categories' not in st.session_state:
        st.session_state.smae_categories = {}

    # for category in smae_categories.keys():
    #     identifier = replace_spaces_and_commas_with_underscores(category)
        
    #     st.session_state.smae_categories[identifier] = st.slider(f"Cantidad de {category}", 0, 10, label_visibility='hidden')
        
    #     maximum = calculate_max(category, identifier, limits)
    #     st.write(get_text_color(maximum, category))
        
   
    col1, col2, col3 = st.columns([3,5,3])

    
    # Iterate over categories
    for category in smae_categories.keys():
        identifier = replace_spaces_and_commas_with_underscores(category)    

        with col1:    
            # Display buttons for decreasing amount
            st.button(f"{category} - 1", key=f"{identifier}_reduce")
            if st.session_state.smae_categories[identifier] >= 1:
                if st.session_state[f"{identifier}_reduce"]:
                    st.session_state.smae_categories[identifier] -= 1

        with col3:
            # Display buttons for increasing amount
            st.button(f"{category} + 1", key=f"{identifier}_increase")
        
            # Check button clicks and update size accordingly
            if st.session_state.smae_categories[identifier] >= 0:
                if st.session_state[f"{identifier}_increase"]:
                    st.session_state.smae_categories[identifier] += 1
                    
    
    # Iterate over categories
    for category in smae_categories.keys():
        identifier = replace_spaces_and_commas_with_underscores(category)    
        
        # In the first column, display information
        with col2:
            maximum = calculate_max(category, identifier, limits)
            st.write(get_text_color(maximum, category))      
  
        
    for macro in limits: 
        
        current_macros, _ = calculate_current_macros(macro)
        st.write(f"{macro}: {current_macros}")  
        # text_to_show = get_text_to_show(identifier, current_amount)
          
        # Use st.progress for the progress bar
        # st.progress(percentage_of_max_lim, text=text_to_show)    




if __name__ == "__main__":
    main()
    
#%%
# python -m streamlit run C:\Users\52331\Documents\GitHub\NutOpt\streamlit_category_estimation.py