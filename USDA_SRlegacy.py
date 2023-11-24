# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 15:04:28 2023

@author: Oscar Flores

This File generates a single csv containing only information on the category
Food name and all the Nutrients as columns. 
"""

import pandas as pd

directory = r'C:\Users\52331\Documents\GitHub\NutOpt\\'

#%% Fetch data

food = pd.read_csv(directory + 'food.csv')
food_nutrient = pd.read_csv(directory + 'food_nutrient.csv')
nutrient = pd.read_csv(directory + 'nutrient.csv')
food_portion = pd.read_csv(directory + 'food_portion.csv')

# Not used yet though
food_category = pd.read_csv(directory + 'food_category.csv')

#%% Merge and clean 
desired_columns = ['description_y', 'description_x', 'name', 'amount', 'unit_name']
merged_nutrients = food_nutrient.merge(nutrient, left_on = 'nutrient_id', right_on='id')    \
                .merge(food)                                                                \
                .merge(food_category, left_on = 'food_category_id', right_on='id')
filtered = merged_nutrients[desired_columns]

filtered = filtered.rename(columns={
    'description_y': 'CATEGORY', 
    'description_x': 'FOOD_NAME', 
    'name': 'NUTRIENT', 
    'amount': 'value', 
    'unit_name': 'UNIT'})

#%% Pivot table
pivoted = filtered.pivot(index=['CATEGORY', 'FOOD_NAME'], columns = ['NUTRIENT', 'UNIT'], values=['value'])
pivoted_copy = pd.DataFrame(pivoted.values, columns = [i[1] +'(' +i[2] + ')' for i in pivoted.columns], index = pivoted.index) #rename columns

pivoted_copy.to_csv(directory + 'FINAL_USDA_MERGED_SR_LEGACY.csv')