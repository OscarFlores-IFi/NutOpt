# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 00:31:14 2023

@author: 52331
"""

import requests
from bs4 import BeautifulSoup
import time
import json
import ast


domain = 'https://avena.io'

#%% First approach, get as most links of recipes as possible. Later we will use only the recommended.
# def extract_links(url, css_selector, delay_seconds = 5):
#     # Send a GET request to the URL
#     response = requests.get(url)

#     # Check if the request was successful (status code 200)
#     if response.status_code == 200:
#         # Parse the HTML content of the page
#         soup = BeautifulSoup(response.text, 'html.parser')

#         # Extract elements based on the CSS selector
#         links = soup.select(css_selector)

#         # Print or process the links as needed
#         for link in links:
#             link_url = link.get('href')  # Get the 'href' attribute
#             link_text = link.get_text()  # Get the text within the link
#             print(f"Link URL: {link_url}, Link Text: {link_text}")
        
#         return links
#     else:
#         print(f"Error: Unable to fetch the content. Status code: {response.status_code}")

#     # Introduce a delay between requests
#     time.sleep(delay_seconds)

# URLs = ['/receta/recetas-bajas-grasa',
#         '/receta/recetas-altas-proteina',
#         '/receta/recetas-keto' ,
#         '/receta/recetas-para-diabetes']

# css_selector = "html body main.box__body div.list__container div.recipes__grid a.recipe__container"

# url_lists = []
# for url in URLs:
#     url_lists.append(extract_links(domain + url, css_selector))
#%% Clean them and get only the links

# recipe_urls = []
# for url_list in url_lists:
#     for link in url_list:
#         recipe_urls.append(link.get('href'))
        

#%%
def save_extracted_data(data, filename):
    with open(filename, 'w') as file:
        if isinstance(data, list):
            # If data is a list, save it directly
            json.dump(data, file, indent=2)
        elif isinstance(data, dict):
            # If data is a dictionary, convert Tag objects to strings before saving
            data_as_strings = {key: str(value) for key, value in data.items()}
            json.dump(data_as_strings, file, indent=2)
        else:
            print("Unsupported data type. Only lists and dictionaries are supported.")


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


#%% save links
# save_to_file(recipe_urls, filename="scraped_links.json")

#%% load links
recipe_urls = load_from_file(filename="scraped_links.json")
recipes_database = load_from_file(filename="avena_recipes_database.json")
#%% 

def scrape_recipes(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # response = requests.get(url_to_scrape)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract recipe title
        recipe_title_element = soup.select_one('html body main.box__body section.recipeTitle__container div.macrosTitle__container--right h1#title')
        recipe_title = recipe_title_element.text if recipe_title_element else "Unknown Recipe Title"
    
    
        # Extract recipe details
        recipe_detail_element = soup.select_one('html body main.box__body div.recipeDetail__containerLayout')
        recipe_detail = recipe_detail_element.text if recipe_detail_element else "No recipe details available"
        # Extract ingredients
        ingredients = {}
        optionals = []
        ingredient_elements = soup.select('html body main.box__body div.recipeDetail__containerLayout div.recipeDetail__ingredientsContainer div.ingredient__info--row')
        for ingredient_element in ingredient_elements:
            try:
                
                skip_element = ingredient_element.find('div', style='font-size: x-small;')
                if skip_element and skip_element.text.strip() == 'Marca y producto sugerido':
                    continue
                ingredient_name = ingredient_element.select_one('div.ingredient__inputContainer div.ingredient__name').text
                amount_value = ingredient_element.select_one('div.ingredient__inputContainer input.ingredient__info--input').get('value', '')
                unit_value = ingredient_element.select_one('div.ingredient__inputContainer div.ingredient__unity').text
                link_href = ingredient_element.select_one('div.ingredient__info--row a.ingredient__seeIngredient').get('href', '')

                ingredients[ingredient_name] = {
                    'amount': amount_value,
                    'unit': unit_value,
                    'link': link_href
                }
            except:
                optional_ingredient_name = ingredient_element.select_one('div.ingredient__inputContainer div.ingredient__name').text
                optionals.append(optional_ingredient_name)
        ingredients['optional'] = optionals
                 
     
        # Extract information from tables
        macros_tables = soup.select('html body main.box__body div.recipeDetail__containerLayout table.macros__container')
        macros_data = {}
        
        for table in macros_tables:
            rows = table.select('tr.ingredient__info--row')
            for row in rows:
                columns = row.find_all(['th', 'td'])
                if columns:
                    key = columns[0].text.strip()
                    value = columns[1].text.strip()
                    macros_data[key] = value
        
        # Store the recipe in a dictionary
        recipe_data = {
            'title': recipe_title,
            'details': recipe_detail,
            'ingredients': ingredients,
            'macros': macros_data
            
        }
        
        
        suggested_links = [link.get('href') for link in soup.select("html body main.box__body div.ingredients__relatedContainer div.recipes__grid a.recipe__container")]
        
        print(f"Successful extraction for {recipe_title}")
        return (recipe_data, suggested_links)

    else:
        print(f"Error: Unable to fetch {domain + url}. Status code: {response.status_code}")
        return None


#%%%
###############################################################################
###############################################################################
###############################################################################
###############################################################################
# recipes_database = {}
###############################################################################
###############################################################################
###############################################################################
###############################################################################

#%%

cont = 0

for url in recipe_urls:
    if url not in recipes_database.keys():
        recipe_data, suggested_links = scrape_recipes(domain + url)
        
        recipes_database[url] = recipe_data
        
        for suggestion in suggested_links:
            if suggestion not in recipe_urls:
                recipe_urls.append(suggestion)
        
        cont += 1 
         
        time.sleep(5)
        print(len(recipes_database.keys()),len(recipe_urls))
        if cont%1 == 0:
            
            # save links
            save_extracted_data(recipe_urls, filename="scraped_links.json")
            save_extracted_data(recipes_database, filename="avena_recipes_database.json")
            

        