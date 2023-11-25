# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 13:30:57 2023

@author: Oscar Flores

Analysis using only the processed file on foods.
"""


from scipy.optimize import minimize
import pandas as pd
import numpy as np

directory = r'C:\Users\52331\Documents\GitHub\NutOpt\\'

#%% Fetch data

df_usda = pd.read_csv(directory + 'FINAL_USDA_MERGED_SR_LEGACY.csv')

#%% Getting information of the entries that contain the food item we want.
keyword = 'salmon'
candidates = df_usda[df_usda['FOOD_NAME'].str.lower().str.contains(keyword.lower())]

if candidates.shape[0]<10:
    print(candidates[['FOOD_NAME']])
    
#%% List of items we want:

columns_of_interest = df_usda.columns 
    
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
    2618,
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
    7337,
    7326,
    7328,
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

filtered = df_usda[columns_of_interest].loc[item_list].fillna(0)

#%% Setting a random amount of consumption to calculate the total for each nutrient

# amounts = pd.DataFrame(np.random.randint(min_rand,max_rand,len(item_list)),index=filtered.index, columns = ['Amount']) # beautiful solution
amounts = np.random.random(len(item_list)) # required format for optimizer. But does not look nice. 

def calculate_nutrient_scores(food_quantities):
    # Your nutrient scoring function
    # This function should take food quantities as input and return nutrient scores
    # Replace this with your actual nutrient scoring logic
    nutrient_scores = (food_quantities.T.dot(filtered.iloc[:,2:]))
    return nutrient_scores

print(calculate_nutrient_scores(amounts))
#%% DRI limits
CD = 1800 # Abbreviation for Calorie Diet. 

limits = pd.DataFrame({
    'Protein(G)':[CD*0.10/4,CD*0.35/4],                      # 10% to 35% of calorie intake, 4 calories per gram of protein.
    'Energy(KCAL)':[CD*0.95, CD*1.05],                       # I guess it's ok if we deviate 5% from the required intake. 
    'Fatty acids, total saturated(G)':[CD*0.04/9,CD*0.06/9],
    'Total lipid (fat)(G)':[0,CD*0.30/9],                    # 10% to 30% of calorie intake, 9 calories per gram of fat.
    'Carbohydrate, by difference(G)':[CD*0.45/4,CD*0.65/4],  # 45% to 65% of calorie intake, 4 calories per Carb.  
    'Vitamin A, IU(IU)':[CD,CD*3],
    'Vitamin C, total ascorbic acid(MG)':[CD/60,CD/30],
    'Fatty acids, total monounsaturated(G)':[CD*0.15/9,CD*0.20/9],
    'Fatty acids, total polyunsaturated(G)':[CD*0.05/9,CD*0.10/9], 
    },
    index=['LOW', 'HIGH']).T
    


"""
Just as a future reference, some links where I can consult important stuff.

USDA data download
https://fdc.nal.usda.gov/download-datasets.html

National Institutes of Health. (info on Reference Intakes)
https://www.ncbi.nlm.nih.gov/books/NBK545442/
"""
#%%

objective_function = lambda amounts: (amounts>0.1).sum()

high_cons = [{'type': 'ineq', 'fun': lambda x: limits['LOW'][i] - filtered[i].dot(x)} for i in filtered.iloc[:,2:]]
low_cons = [{'type': 'ineq', 'fun':  lambda x: filtered[i].dot(x) - limits['HIGH'][i]} for i in filtered.iloc[:,2:]]
cons = high_cons.append(low_cons)

results = minimize(objective_function, amounts,  constraints= cons, bounds=[(0,10) for i in range(len(item_list))])

results_df = pd.DataFrame(results.x, index=item_list)
print(calculate_nutrient_scores(results.x))


#%%

# from pymoo.algorithms.soo.nonconvex.pso import PSO
# from pymoo.problems.single import Rastrigin
# from pymoo.optimize import minimize

# problem = Rastrigin()

# algorithm = PSO()

# res = minimize(problem,
#                algorithm,
#                seed=1,
#                verbose=False)