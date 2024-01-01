# NutOpt
Yet another Nutritional Optimizer. As all the already available in github, but made by me :)

Sorry for the inconvenience, but I haven't dedicated enough time to make this beautifully packaged, so everything is just a mess by now. 
Important files we have to run are the streamlit ones. Specially: 
- streamlit_app_avena2.py 
- streamlit_category_estimation.py
The first one is an optimizer that given some constraints for each food category, it provides a mix of recipes (scraped from the website of Avena Mx) that satisfy all our needs. The suggestion is random so every time we run the optimizer we get a new set of recipies that satisfy all our requirements. 
The second streamlit is still an ongoing project which resulted harder than I expected, still researching on it. It should dynamically provide the minimum and maximum range of each category of food given some constraints. Similar to the problem before, but this one is the base for the previous one. So for example, if we have a Diet of 2200 Calories, then we can get a diet with Vegetables, Fruits, Cereals, Meats, and Oils that satisfy still with the official requirements (DRI, Daily Recommended Intake of Proteins, Fats, Carbohidrates). All this calculations are right now based on the SMAE (Sistema Mexicano de Alimentos Equivalentes). 


Just as a future reference, some links where I can consult important stuff.

USDA data download
https://fdc.nal.usda.gov/download-datasets.html

National Institutes of Health. (info on Reference Intakes)
https://www.ncbi.nlm.nih.gov/books/NBK545442/
