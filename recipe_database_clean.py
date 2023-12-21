# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 19:39:24 2023

@author: 52331
"""

import json
# from bs4 import BeautifulSoup
import ast
import re

def load_from_file(filename):
    try:
        with open(filename, 'r') as file:
            loaded_data = json.load(file)

        # Check if the loaded data is a dictionary with string values
        if isinstance(loaded_data, dict) and all(isinstance(value, str) for value in loaded_data.values()):
            # Convert strings back to dictionaries using ast.literal_eval
            loaded_data = {key: ast.literal_eval(value) for key, value in loaded_data.items()}

        return loaded_data
    except FileNotFoundError:
        return None

# Load the links back from the file
recipes_database = load_from_file("avena_recipes_database.json")

def convert_to_number(value_with_unit):
    try:
        # Split the value into numeric and unit parts
        numeric_value, unit = value_with_unit.split()

        # Convert the numeric part to a float
        numeric_value = float(numeric_value)

        return numeric_value
    except ValueError:
        # Handle the case where conversion fails
        return 0

def get_calories(title):
    # Use regular expression to extract the numerical value
    calories_match = re.search(r'\b(\d+(\.\d+)?)\s*Kcal\b', title)
    
    # Check if a match is found
    if calories_match:
        # Extract the matched numerical value as an integer
        calories = float(calories_match.group(1))
        return(calories)
        print(calories)
    else:
        print("No calories information found in the title.")


#%%
foods = {}
for key, item in recipes_database.items():
    if len(item['ingredients']) > 5:
        nuevos_macros = {}
        calorias = get_calories(item['title'])
        nuevos_macros['Calorias'] = calorias
        for nutrient, value in item['macros'].items():
            nuevos_macros[nutrient] = convert_to_number(value)
        foods[key] = nuevos_macros

with open("avena_food_nutrients.json", "w") as file:
    json.dump(foods, file)
    
#%%
mult = 1
CD=1800*mult


limits2 = {
    'Calorias':{'min':int(CD*0.95),'max':int(CD)},
    'Proteinas':{'min':int(CD*0.10/4),'max':int(CD*0.35/4)},
    'Carbohidratos':{'min':int(CD*0.45/4),'max':int(CD*0.65/4)},
    'Fibra':{'min':25*mult,'max':500*mult},
    'Potasio':{'min':2000*mult,'max':10000*mult},
    'Calcio':{'min':1000*mult,'max':5000*mult},
    'Grasas monoinsaturadas':{'min':int(CD*0.15/9),'max':int(CD*0.20/9)},
    'Grasas poliinsaturadas':{'min':int(CD*0.05/9),'max':int(CD*0.10/9)},
    'Grasas saturadas':{'min':int(CD*0.04/9),'max':int(CD*0.06/9)},
    'Colesterol':{'min':0*mult,'max':300*mult},
    'Vitamina A':{'min':int(CD),'max':int(CD*3)},
    'Sodio':{'min':0*mult,'max':300*mult},
    'Vitamina B6':{'min':2*mult,'max':12*mult},
    'Vitamina B12':{'min':0*mult,'max':1000*mult},
    'Magnesio':{'min':0*mult,'max':400*mult},
    'Tiamina':{'min': 0*mult,'max':12*mult},
    'Riboflavina':{'min':0.6*mult,'max':3*mult},
    'Niacina':{'min':0*mult,'max':30*mult},
    'Folato':{'min':0*mult,'max':1000*mult},
    'Zinc':{'min':0*mult,'max':40*mult},
    }

with open("avena_nutrition_constraints.json", "w") as file:
    json.dump(limits2, file)
