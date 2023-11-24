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
    'protein': {'min': 30, 'max': 50},
    'carbs': {'min': 40, 'max': 60},
    'fat': {'min': 10, 'max': 20},
}

def optimize_diet(food_quantities):
    # Define decision variables
    x = food_quantities

    # Set up the coefficients for the objective function
    c = [-food['cost'] for food in foods.values()]

    # Set up the inequality constraints matrix
    A = [
        [-food['protein'] for food in foods.values()],
        [-food['carbs'] for food in foods.values()],
        [-food['fat'] for food in foods.values()],
    ]

    # Set up the inequality constraints vector
    b = [-nutrient_constraints['protein']['min'], -nutrient_constraints['carbs']['min'], -nutrient_constraints['fat']['min']]

    # Bounds for the decision variables
    x_bounds = [(0, None) for _ in range(len(foods))]

    # Solve the linear programming problem
    result = linprog(c, A_ub=A, b_ub=b, bounds=x_bounds, method='highs', x0=x)

    if result.success:
        return result.fun, result.x
    else:
        return float('inf'), None

# Streamlit app
def main():
    st.title("Nutritional Optimization App")

    # User input for food quantities
    food_quantities = {}
    for food in foods:
        food_quantities[food] = st.slider(f"Quantity of {food}", 0, 100, 0)

    # Button to optimize
    if st.button("Optimize"):
        # Get the user-defined food quantities
        user_quantities = [food_quantities[food] for food in foods]

        # Optimize the diet
        cost, optimized_quantities = optimize_diet(user_quantities)

        # Display results
        st.subheader("Optimization Results:")
        st.write(f"Total Cost: {cost:.2f}")
        st.write("Optimal Food Quantities:")
        for i, quantity in enumerate(optimized_quantities):
            st.write(f"{list(foods.keys())[i]}: {quantity}")

if __name__ == "__main__":
    main()
