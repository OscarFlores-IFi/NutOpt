# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 13:30:57 2023

@author: 52331

Analysis using only the processed file on foods. 
"""


import pandas as pd

directory = r'C:\Users\52331\Downloads\FoodData_Central_sr_legacy_food_csv_2018-04\FoodData_Central_sr_legacy_food_csv_2018-04\\'

#%% Fetch data

df_usda = pd.read_csv(directory + 'FINAL_USDA_MERGED_SR_LEGACY.csv')

#%% Cleaning unwanted products

columns_of_interest =[
    'CATEGORY',
    'FOOD_NAME',
    'Protein(G)',
    'Energy(KCAL)',
    'Water(G)',
    'Fatty acids, total saturated(G)',
    'Total lipid (fat)(G)',
    'Carbohydrate, by difference(G)',
    'Vitamin A, IU(IU)',
    'Vitamin C, total ascorbic acid(MG)',
    'Fatty acids, total monounsaturated(G)',
    'Fatty acids, total polyunsaturated(G)',
    'Magnesium, Mg(MG)',
    'Manganese, Mn(MG)',  
    ]

categories_of_interest = [
    'Baked Products', 
    'Beef Products', 
    'Cereal Grains and Pasta',
    'Dairy and Egg Products', 
    'Fats and Oils', 
    'Finfish and Shellfish Products', 
    'Fruits and Fruit Juices',
    'Legumes and Legume Products', 
    'Nut and Seed Products', 
    'Pork Products', 
    'Poultry Products', 
    'Vegetables and Vegetable Products'
    ]

non_wanted_attributes = [
    'artificial',
    'Archway',
    'andrea',
    'angelfood',
    'Heinz', 
    'Keebler',
    'keikitos',
    'kraft',
    'Martha', 
    'Mary', 
    'Mckee',
    'Nabisco',
    'ricura',
    'Pepperidge',
    'commercial',
    'pillsbury',
    'valley', 
    'udi\'s',
    'van\'s',
    'wonton',
    'reddi',
    'industrial',
    'alaska',
    'canned', 
    'bottled',
    'ocean spray',
    'bolthouse',
    'naked juice', 
    'odwalla',
    'sweetened',
    'unsweetened',
    'steweed',
    'sulfured',
    'syrup',
    'concentrate',
    'boiled',
    'cooked',
    'house foods',
    'mori-nu',
    'silk ',
    'vitasoy', 
    'hormel',
    'bbq',
    'mars snackfood',
    'slim-fast',
    'power bar',
    'formulated',
    'drained',
    ]

df_usda_cat = df_usda[(df_usda['CATEGORY'].isin(categories_of_interest)) & 
                      (pd.concat([df_usda['FOOD_NAME'].str.lower().str.contains(i.lower()) for i in non_wanted_attributes], axis=1).sum(axis=1)==0)]
df_usda_cat = df_usda_cat[columns_of_interest]

corr_mat = df_usda_cat.corr()



#%% Getting information of the entries that contain the food item we want.

# We need to filter only for certain foods. This work is quite manual, so 
# we better get all the values by finding if they contain our keywords
keyword = 'grapef'
candidates = df_usda[df_usda['FOOD_NAME'].str.lower().str.contains(keyword.lower())]

if candidates.shape[0]<10:
    print(candidates[['FOOD_NAME']])
    
#%% List of items we want:
    
item_list = [
    2120,3826,3827,3828,3830,
    4097,
    2118,2968,2969,2980,2988,3155,3232,
    3861,3862,3869,3898,3900,3903,4136,4151,
    4036,4037,4038,4159,
    2115,3409,3949,3966,3969,3970,
    3992,
    3858,6178,
    3987,3986,4160,
    3854,3856,3855,
    4007,4005,
    4066,4077,4043,
    4116,4011,4118,
    3853,6863,3892,4063,
    3920,
    ]


filtered = df_usda[columns_of_interest].loc[item_list]
unprocessed = filtered[filtered['FOOD_NAME'].str.contains(' raw')]





#%% DRI 
Fat = [20,35]
Polyunsaturated_fatty_acids_n_6 = [5,10]
Polyunsaturated_fatty_acids_n_3 = [0.6,1.2]
Carbohydrate = [45,65]
Protein = [10,35]


"""
Just as a future reference, some links where I can calculate important stuff.

USDA data download
https://fdc.nal.usda.gov/download-datasets.html

National Institutes of Health. (info on Reference Intakes)
https://www.ncbi.nlm.nih.gov/books/NBK545442/



"""