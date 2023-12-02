# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 22:19:44 2023

@author: Oscar Flores

This is the draft that will later become a front end for the optimizer
"""
import streamlit as st
import json
from scipy.optimize import linprog

#%% Read files

# Food nutritional facts
with open('food_nutrients.json', 'r') as file:
    foods = json.load(file)
    
# Nutritional constraints
with open("nutrition_constraints.json", "r") as file:
    nutrient_constraints = json.load(file)

#%% Define functions

# Function to replace spaces and commas with underscores
def replace_spaces_and_commas_with_underscores(text):
    return text.replace(" ", "_").replace(",", "_")

# Function to replace underscores with spaces
def replace_underscores_with_spaces(text):
    return text.replace("_", " ")

# Function to calculate the current nutrient amount based on user-defined food quantities
def calculate_current_amount(nutrient):
    current_value = sum(foods[food][nutrient] * st.session_state.food_quantities.get(food, 0) for food in foods)
    percentage = (current_value / (nutrient_constraints[nutrient]['max']*1.3))
    if percentage < 1:
        return (current_value, percentage)
    return (current_value, 100)


def get_text_to_show(identifier, current_amount):
    min_limit, max_limit = st.session_state.nutrient_limits[identifier]
    if current_amount < min_limit:
        return ":orange[below limits]"  
    elif current_amount > max_limit:
        return ":orange[above limits]"      
    else:
        return ":green[within limits]"

def optimize_food_consumption(foods, selected_foods, nutrient_constraints):
    """
    Parameters
    ----------
    food_nutrient_facts : pd.DataFrame
        Contains information of at least, each of the variables of interest, 
        for each food. In the Rows we expect the food, as a column the nutrient.
        
    limits : pd.DataFrame
        As many rows as Nutrient limits we have. Two columns, one for the 
        high limit, one for the low limit. 

    Returns
    -------
    np.array
        with information on the optimal allocation of each food to satisfy the 
        defined constraints.

    """
    

    
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
        
        current_amount, _ = calculate_current_amount(nutrient)
        
        rhs_ineq.append(limits['max']-current_amount)
        rhs_ineq.append(current_amount - limits['min'])
        
    # Minimization of objective Function
    obj = [-1]* len(lhs_ineq[0])
    
    # # Inequalities. Lhs smaller or equal than Rhs.
    # lhs_ineq1 = food_nutrient_facts[inequality_vars].T.values # Smaller than
    # lhs_ineq2 = -food_nutrient_facts[inequality_vars].T.values # Bigger than
    # rhs_ineq1 = limits.loc[inequality_vars]['max'].values
    # rhs_ineq2 = -limits.loc[inequality_vars]['min'].values
    
    # lhs_ineq = np.concatenate((lhs_ineq1, lhs_ineq2))
    # rhs_ineq = np.concatenate((rhs_ineq1, rhs_ineq2))
    
    # # Equalities. Only for Calorie consumption. 
    # lhs_eq = food_nutrient_facts['Energy(KCAL)'].values.reshape((1,food_nutrient_facts.shape[0]))
    # rhs_eq = [CD]
    
    # Boundaries. Maximum 300 grams of any given product per day.
    bnd = [(0,300)]*len(lhs_ineq[0])
    
    opt = linprog(c=obj, 
                  A_ub=lhs_ineq, 
                  b_ub=rhs_ineq,
                  bounds=bnd,
                  method="highs")
    
    print(opt.x.dtype)
    
    opt.x
    # return opt.x
    pass


#%% Streamlit app
def main():
    st.title("Nutritional Optimization App")

    # Dropdown for selecting a food
    selected_food = st.selectbox("Select a food:", list(foods.keys()))
    
    # Create or get the food_quantities dictionary from session state
    if 'food_quantities' not in st.session_state:
        st.session_state.food_quantities = {}

    # User input for food quantities
    if selected_food in st.session_state.food_quantities:
        st.session_state.food_quantities[selected_food] = st.slider(f"Quantity of {selected_food}", 0, 400, st.session_state.food_quantities[selected_food])
    else:
        st.session_state.food_quantities[selected_food] = st.slider(f"Quantity of {selected_food}", 0, 400, 0)

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
   
        current_amount, percentage_of_max_lim = calculate_current_amount(nutrient)
        
        text_to_show = get_text_to_show(identifier, current_amount)
        
        # Use st.progress for the progress bar
        st.progress(int(percentage_of_max_lim*100), text=text_to_show)    


    for nutrient, limits in nutrient_constraints.items():
        st.write(f"{nutrient}: {limits}")

    # # Button to optimize
    if st.button("Optimize"):
        optimize_food_consumption(foods, st.session_state.food_quantities, nutrient_constraints)
    #     # Get the user-defined food quantities
    #     user_quantities = [food_quantities[food] for food in foods]

    #     # Get the user-defined nutrient limits
    #     user_limits = [nutrient_limits[nutrient] for nutrient in nutrient_constraints]

    #     # Optimize the diet
    #     cost, optimized_quantities = optimize_diet(user_quantities, user_limits)

    #     # Display results
    #     st.subheader("Optimization Results:")
    #     st.write(f"Total Cost: {cost:.2f}")
    #     st.write("Optimal Food Quantities:")
    #     for i, quantity in enumerate(optimized_quantities):
    #         st.write(f"{list(foods.keys())[i]}: {quantity}")

    # return None

if __name__ == "__main__":
    main()
    
    

# filtered['Solution'] = optimize_food_consumption(filtered, limits)

# calculate_nutrient_scores(filtered, filtered['Solution'])

#%%
# python -m streamlit run C:\Users\52331\Documents\GitHub\NutOpt\streamlit_app.py