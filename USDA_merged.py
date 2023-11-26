# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 13:30:57 2023

@author: Oscar Flores

Analysis using only the processed file on foods.
"""



# from scipy.optimize import minimize
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
# from pymoo.algorithms.soo.nonconvex.pso import PSO
# from pymoo.problems.single import Rastrigin
# from pymoo.optimize import minimize


directory = r'C:\Users\52331\Documents\GitHub\NutOpt\\'

#%% Fetch data

df_usda = pd.read_csv(directory + 'FINAL_USDA_MERGED_SR_LEGACY.csv')

#%% Getting information of the entries that contain the food item we want.
keyword = 'salmon'
candidates = df_usda[df_usda['FOOD_NAME'].str.lower().str.contains(keyword.lower())]

if candidates.shape[0]<10:
    print(candidates[['FOOD_NAME']])
    
#%% List of items we want:

columns_of_interest = [
    'CATEGORY', 
    'FOOD_NAME',
    'Protein(G)',
    'Cholesterol(MG)',
    'Fiber, total dietary(G)',
    'Fatty acids, total trans(G)',
    'Iron, Fe(MG)',
    'Sodium, Na(MG)',
    'Fatty acids, total saturated(G)',
    'Carbohydrate, by difference(G)',
    'Energy(KCAL)',
    'Water(G)',
    'Sugars, Total(G)',
    'Vitamin A, IU(IU)',
    'Vitamin C, total ascorbic acid(MG)',
    'Calcium, Ca(MG)',
    'Fatty acids, total monounsaturated(G)',
    'Fatty acids, total polyunsaturated(G)',
    'Thiamin(MG)',
    'Total lipid (fat)(G)',
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
filtered.to_csv(directory + 'SMALL_DATASET.csv')

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

#%% Limits

CD=1800

columns_of_interest = {
    'Protein(G)':[CD*0.10/4,CD*0.35/4],
    'Cholesterol(MG)':[0,300],
    'Fiber, total dietary(G)':[25,np.inf],
    'Fatty acids, total trans(G)':[0,0.01*CD/9],
    'Iron, Fe(MG)':[18,np.inf],
    'Sodium, Na(MG)':[0,300],
    'Fatty acids, total saturated(G)':[CD*0.04/9,CD*0.06/9],
    'Carbohydrate, by difference(G)':[CD*0.45/4,CD*0.65/4],
    'Energy(KCAL)':[CD*0.95, CD*1.05],
    'Water(G)':[0,2500],
    'Sugars, Total(G)':[0,50],
    'Vitamin A, IU(IU)':[CD,CD*3],
    'Vitamin C, total ascorbic acid(MG)':[CD/60,CD/30],
    'Calcium, Ca(MG)':[1000,np.inf],
    'Fatty acids, total monounsaturated(G)':[CD*0.15/9,CD*0.20/9],
    'Fatty acids, total polyunsaturated(G)':[CD*0.05/9,CD*0.10/9],
    'Thiamin(MG)':[0,np.inf],
    'Total lipid (fat)(G)':[0,CD*0.30/9],
    }

#%% Classification Excercise. Many 'Similar products'

# X = df_usda.fillna(0).iloc[:,2:].drop(columns='Water(G)')

# db = DBSCAN(eps=0.001, min_samples=5, metric='cosine', n_jobs=-1).fit(X)
# # db = DBSCAN(eps=10, min_samples=2, metric='euclidean', n_jobs=-1).fit(X)
# labels = db.labels_
# # Number of clusters in labels, ignoring noise if present.
# n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
# n_noise_ = list(labels).count(-1)

# print("Estimated number of clusters: %d" % n_clusters_)
# print("Estimated number of noise points: %d" % n_noise_)

# unique_labels = set(labels)
# core_samples_mask = np.zeros_like(labels, dtype=bool)
# core_samples_mask[db.core_sample_indices_] = True

# colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
# for k, col in zip(unique_labels, colors):
#     if k == -1:
#         # Black used for noise.
#         col = [0, 0, 0, 1]

#     class_member_mask = labels == k

#     xy = X[class_member_mask & core_samples_mask]
#     plt.plot(
#         xy['Total lipid (fat)(G)'],
#         xy['Energy(KCAL)'],
#         "o",
#         markerfacecolor=tuple(col),
#         markeredgecolor="k",
#         markersize=14,
#     )

#     xy = X[class_member_mask & ~core_samples_mask]
#     plt.plot(
#         xy['Total lipid (fat)(G)'],
#         xy['Energy(KCAL)'],
#         "o",
#         markerfacecolor=tuple(col),
#         markeredgecolor="k",
#         markersize=6,
#     )

# plt.title(f"Estimated number of clusters: {n_clusters_}")
# plt.show()

# df_labeled = df_usda[columns_of_interest].join(pd.DataFrame(labels))

#%% 

