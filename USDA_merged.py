# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 13:30:57 2023

@author: Oscar Flores

Analysis using only the processed file on foods.
"""

import json
import pandas as pd

directory = r'C:\Users\52331\Documents\GitHub\NutOpt\\'

#%% Fetch data

df_usda = pd.read_csv(directory + 'FINAL_USDA_MERGED_SR_LEGACY.csv').fillna(0)

#%% Getting information of the entries that contain the food item we want.
df_usda['FOOD_NAME'] = df_usda['FOOD_NAME'].str.replace("\(Includes foods for USDA\'s Food Distribution Program\)", "")
keyword = 'includes'
candidates = df_usda[df_usda['FOOD_NAME'].str.lower().str.contains(keyword.lower())]

if candidates.shape[0]<10:
    print(candidates[['FOOD_NAME']])
#%% List of items we want:

columns_of_interest = [
    'CATEGORY', 
    'FOOD_NAME',
    'Energy(KCAL)',
    'Protein(G)',
    'Carbohydrate, by difference(G)',
    'Total lipid (fat)(G)',
    'Fatty acids, total monounsaturated(G)',
    'Fatty acids, total polyunsaturated(G)',
    'Fatty acids, total saturated(G)',
    'Fatty acids, total trans(G)',
    'Fiber, total dietary(G)',
    'Cholesterol(MG)',
    'Iron, Fe(MG)',
    'Sodium, Na(MG)',
    'Sugars, Total(G)',
    'Vitamin A, IU(IU)',
    'Vitamin C, total ascorbic acid(MG)',
    'Calcium, Ca(MG)',
    'Thiamin(MG)',
    'Water(G)',
    ]
    
item_list = [
    # Aqui empiezan los sugeridos por la applicacion 'Avena'
    
    4694,   # Leguminosas
    4698,
    4701,
    4716,
    7610,
    4739,
    4758,
    
    2985,   # Lacteos
    3005,
    2939,
    2944,
    2757,
    
    1694,   # Proteina
    1697,
    1545,
    5327,
    2862,
    2746,
    2751,
    2771,
    2778,
    2777,
    2794,
    2800,
    2816,
    3700,
    6117,
    3775,
    3743,
    3751,
    3753,
    3565,
    3782,
    5471,
    5752,
    3695,
    3731,
        
    3400,   # Aceites
    3439,
    4020,
    3856,
    3396,
    3400,
    2766,
    2729,
    3498,
    5152,
    5053,
    5002,
    4787,
    6765,
    4732,
    5095,
    5020,
    5059,
    5080,
    5081,
    5090,
    
    2543,   # Cereales
    2722,
    2660,
    2664,
    2565,
    2578,
    2605,
    625,
    7695,
    810,
    2565,
    532,
    550,
    556,
    578,
    580,
    613,
    798,
    808,
    2631,
    2611,
    6230,
    587,
    7548,
    2707,
    
    3977,   # Frutas
    3862,
    3869,
    3898,
    4136,
    4151,
    4116,
    3892,
    3910,
    3909,
    4063,
    3853,
    4118,
    3920,
    3987,
    3997,
    3996,
    3992,
    4007,
    4044,
    4045,
    4011,
    4159,
    3824,
    3825,
    3826,
    3827,
    3828,
    4098,
    4038,
    4018,
    3858,
    4077,
    4080,
    4081,
    4160,
    3956,
    3970,
    5043,  
    5046,    
    
    6993,   # Verduras
    7151, 
    7082,
    7246,
    7061,
    7773,
    7381,
    7163,
    7111,
    7114,
    7644,
    7573,
    7089,
    7347,
    7418,
    7282,
    7145,
    7428,
    7430,
    7002,
    7625,
    4738,
    4739,
    7297,
    7615,
    6979,
    7734,
    7300,
    7302,
    7228,
    7423,
    7432,
    7430,
    7434,
    7436,
    7443,
    7452,
    7454,
    7292,
    7584,
    7123,
    7133,
    
    7461, # De aqui empiezan los 'opcionales'
    ]

filtered = df_usda[columns_of_interest].loc[item_list]
filtered.to_csv(directory + 'SMALL_DATASET.csv')

#%% Transform data into the shape required in the streamlit app

# Format:
# foods = {
#     'food1': {'protein': 10, 'carbs': 20, 'fat': 5, 'cost': 2},
#     'food2': {'protein': 15, 'carbs': 10, 'fat': 3, 'cost': 3},
#     'food3': {'protein': 5, 'carbs': 30, 'fat': 8, 'cost': 1},
# }

food_dict = {}
for food in filtered['FOOD_NAME'].unique():
    tmp = {}
    for nutrient in columns_of_interest[2:]:
        tmp[nutrient] = filtered[filtered['FOOD_NAME'] == food][nutrient].values[0]/100
    food_dict[food] = tmp

with open("food_nutrients.json", "w") as file:
    json.dump(food_dict, file)
    
    
#%% Limits

CD=1800
# We need a format as:
# nutrient_constraints = {
#     'protein': {'min': 30, 'max': 500},
#     'carbs': {'min': 40, 'max': 600},
#     'fat': {'min': 10, 'max': 200},
# }


limits2 = {
    'Energy(KCAL)':{'min':int(CD*0.95),'max':int(CD)},
    'Protein(G)':{'min':int(CD*0.10/4),'max':int(CD*0.35/4)},
    'Carbohydrate, by difference(G)':{'min':int(CD*0.45/4),'max':int(CD*0.65/4)},
    'Total lipid (fat)(G)':{'min':0,'max':int(CD*0.30/9)},
    'Fatty acids, total monounsaturated(G)':{'min':int(CD*0.15/9),'max':int(CD*0.20/9)},
    'Fatty acids, total polyunsaturated(G)':{'min':int(CD*0.05/9),'max':int(CD*0.10/9)},    'Cholesterol(MG)':{'min':0,'max':300},
    'Fatty acids, total saturated(G)':{'min':int(CD*0.04/9),'max':int(CD*0.06/9)},
    'Fatty acids, total trans(G)':{'min':0,'max':int(0.01*CD/9)},
    'Fiber, total dietary(G)':{'min':25,'max':500},
    'Iron, Fe(MG)':{'min':18,'max':80},
    'Sodium, Na(MG)':{'min':0,'max':300},
    'Sugars, Total(G)':{'min':0,'max':50},
    'Vitamin A, IU(IU)':{'min':int(CD),'max':int(CD*3)},
    'Vitamin C, total ascorbic acid(MG)':{'min':int(CD/60),'max':int(CD/30)},
    'Calcium, Ca(MG)':{'min':1000,'max':5000},
    'Thiamin(MG)':{'min':0,'max':10000},
    'Water(G)':{'min':0,'max':2500},
    }
# To convert into the same format as limits:
# limits2 = pd.DataFrame(limits2).T

with open("nutrition_constraints.json", "w") as file:
    json.dump(limits2, file)
