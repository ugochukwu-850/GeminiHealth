#from reqwest import GET
import csv
import pathlib
from .models import Ingredients

def verify_image(url: str) -> bool:
    # make a request to the endpoint 
    #req = GET(url)
    
    #if req.status != 200:
        #return False
    return True

def populate_ingredients():
    # get the path for both allergy and Ingredients 
    ingredient_data_path = pathlib.Path("./../public_src/FoodData.csv")
    allergy_data_path = pathlib.Path("./../public_src/ingredients.csv")
    
    # read the both of them into memory
    with open(ingredient_data_path, mode="r") as ingredient:
        line = csv.DictReader(ingredient)
        print(line)
        
    with open(allergy_data_path, mode="r") as ingredient:
        line = csv.DictReader(ingredient)
        print(line)