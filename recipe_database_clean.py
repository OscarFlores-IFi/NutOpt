# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 19:39:24 2023

@author: 52331
"""

import json
from bs4 import BeautifulSoup
import ast

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



#%%
foods = {}
for key, item in recipes_database.items():
    nuevos_macros = {}
    for nutrient, value in item['macros'].items():
        nuevos_macros[nutrient] = convert_to_number(value)
    foods[key] = nuevos_macros

with open("avena_food_nutrients.json", "w") as file:
    json.dump(foods, file)
    
#%%
CD=1800

limits2 = {
    'Proteinas':{'min':int(CD*0.10/4),'max':int(CD*0.35/4)},
    'Carbohidratos':{'min':int(CD*0.45/4),'max':int(CD*0.65/4)},
    'Fibra':{'min':0,'max':int(CD*0.30/9)},
    'Potasio':{'min':int(CD*0.15/9),'max':int(CD*0.20/9)},
    'Calcio':{'min':int(CD*0.05/9),'max':int(CD*0.10/9)},    'Cholesterol(MG)':{'min':0,'max':300},
    'Grasas monoinsaturadas':{'min':int(CD*0.04/9),'max':int(CD*0.06/9)},
    'Grasas poliinsaturadas':{'min':0,'max':int(0.01*CD/9)},
    'Grasas saturadas':{'min':25,'max':500},
    'Colesterol':{'min':25,'max':500},
    'Vitamina A':{'min':25,'max':500},
    'Sodio':{'min':25,'max':500},
    'Vitamina B6':{'min':18,'max':80},
    'Vitamina B12':{'min':0,'max':300},
    'Magnesio':{'min':0,'max':50},
    'Tiamina':{'min':int(CD),'max':int(CD*3)},
    'Riboflavina':{'min':int(CD/60),'max':int(CD/30)},
    'Niacina, Ca(MG)':{'min':1000,'max':5000},
    'Folato':{'min':0,'max':10000},
    'Zinc':{'min':0,'max':2500},
    }

with open("nutrition_constraints.json", "w") as file:
    json.dump(limits2, file)
