from django.db import models, IntegrityError
from django.contrib.auth.models import AbstractUser
from pathlib import Path
from .utils import verify_image
import csv

class Metric(models.TextChoices):
    GRAM = 'g', ('Gram') 
    KILOGRAM = 'kg', ('Kilogram')
    MILLIGRAM = 'mg', ('Milligram')
    LITER = 'l', ('Liter')
    MILLILITER = 'ml', ('Milliliter')
    TEASPOON = 'tsp', ('Teaspoon')
    TABLESPOON = 'tbsp', ('Tablespoon')
    CUP = 'cup', ('Cup')
    PINT = 'pt', ('Pint')
    QUART = 'qt', ('Quart')
    GALLON = 'gal', ('Gallon')
    OUNCE = 'oz', ('Ounce')
    POUND = 'lb', ('Pound')
    PINCH = 'pinch', ('Pinch')
    DASH = 'dash', ('Dash')
    FLUID_OUNCE = 'fl oz', ('Fluid Ounce')
    MILLIGALLON = 'mgal', ('Milligallon')
    CLOVE = 'clove', ('Clove')
    BUNCH = 'bunch', ('Bunch')
    PACKET = 'packet', ('Packet')
    NUTMEG = 'nutmeg', ('Nutmeg')
    PIECE = 'piece', ('Piece')
    WHOLE = 'whole', ('Whole')
    SPRIG = 'sprig', ('Sprig')
    HEAD = 'head', ('Head')
    DROPS = 'drops', ('Drops')

class Allergy(models.Model):
    name = models.CharField(max_length=225, unique=True)
    classification = models.CharField(max_length=225)
    topology = models.CharField(max_length=225)
    group = models.CharField(max_length=225)

class Ingredients(models.Model):
    name = models.TextField(unique=True)
    spoonacular_id = models.CharField(max_length=225)
    allergies = models.ManyToManyField(Allergy, related_name="ingredients")
    
    @classmethod
    def populate(self):
        allergies = Path("public_src/FoodData.csv")
        ingredients = Path("public_src/ingredients.csv")
        
        # read the allergies into memory
        with open(allergies, mode="r") as f:
            allergies = csv.DictReader(f)
            all_set = {}
            
            for allergy in allergies:
                                  
                # create a allergy instance
                try:
                    alley = Allergy(name=allergy["Allergy"].strip(), classification=allergy["Class"], topology=allergy["Type"], group=allergy["Group"])

                    alley.save()
                    all_set[str(allergy["Food"].strip().lower())] = alley
                except IntegrityError:
                    all_set[str(allergy["Food"].strip().lower())] = Allergy.objects.all().get(name=allergy["Allergy"])
                
            allergies = all_set
            
        
        with open(ingredients, mode="r") as f:
            ingredients = csv.reader(f)
            all_ingies = []
            
            for ingredient in ingredients:
                ingredient = str(ingredient).strip("'][").split(";")
                
                all_ingies.append({"name": str(ingredient[0]), "id": str(ingredient[1])})
            
            ingredients = all_ingies
            for ingredient in ingredients:
                i_allergy = allergies.get(ingredient["name"].strip().lower())
                try:
                    ingy = Ingredients(name=ingredient["name"], spoonacular_id=ingredient["id"])
                    ingy.save()
                    if i_allergy is not None:
                        ingy.allergies.add(i_allergy)
                except IntegrityError:
                    ingy = Ingredients.objects.get(name=ingredient["name"])
                    if i_allergy is not None:
                        ingy.allergies.add(i_allergy)
                
        
      
                    
            
        
        

class Nutrients(models.Model):
    name = models.CharField(max_length=100, unique=True)

class MedicalCondition(models.Model):
    name = models.CharField(max_length=100, unique=True)
    diagnose_date = models.DateField()
    learn_more = models.URLField()
    explanation = models.TextField(null=False, blank=False)

class Medication(models.Model):
    name = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    condition = models.ForeignKey(MedicalCondition, related_name='medications', on_delete=models.CASCADE)

  


class User(AbstractUser):
    username = models.TextField()
    email = models.EmailField(unique=True)
    is_company = models.BooleanField(default=False)
    account_balance = models.PositiveIntegerField(default=1000)
    image_url = models.URLField(default="https://fund-rest-framework.s3.amazonaws.com/ev.energy_logo.png")
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    long = models.DecimalField(max_digits=9, decimal_places=6)
    # Other User fields go here...
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "password", "lat", "long"]
    
    def save(self, *args, **kwargs):
        
        # Check if the password has been set or changed
        if self._state.adding or self.password != self._password:
            self.set_password(raw_password=self.password)
        # check that the image is indeed an image or set a default link
        if verify_image(self.image_url):
            self.image_url = "https://example.com/profile_image.jpg"
        super().save(*args, **kwargs)  
            
class MedicalProfile(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="medical_profiles")
    conditions = models.ManyToManyField(MedicalCondition, related_name="medical_profiles")
    dietary_highlights = models.TextField()
    summary = models.TextField()
    food_allergies = models.ManyToManyField(Allergy)  

class MedicalNutrientNeedItem(models.Model):
    nutrient = models.ManyToManyField(Nutrients, related_name="nutrient_items")
    amount = models.PositiveIntegerField(null=True)
    metric = models.CharField(choices=Metric.choices, default=Metric.GRAM, max_length=10)
    medicalprofile = models.ForeignKey(MedicalProfile, related_name="nutritional_needs", on_delete=models.CASCADE)

class Company(models.Model):
    admin = models.OneToOneField(User, related_name="company", on_delete=models.CASCADE)
    cover_photo = models.URLField()
    profile_photo = models.URLField()
    name = models.CharField(max_length=225)
    about = models.TextField(null=True)
    joined = models.DateTimeField(auto_now=True)

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    preparation_method = models.CharField(choices=Metric.choices, null=True, max_length=255)
    ingredients = models.ManyToManyField(Ingredients, related_name="recipes")
    company = models.ForeignKey(Company, related_name="recipes", on_delete=models.CASCADE)

class Store(models.Model):
    last_updated = models.DateTimeField(auto_now_add=True)

class StoreItem(models.Model):
    store = models.ForeignKey(Store, related_name="items", on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredients, related_name="stock", on_delete=models.CASCADE)
    date_in = models.DateTimeField(auto_now=True)
    amount = models.PositiveIntegerField()
    metric = models.CharField(choices=Metric.choices, default=Metric.GRAM, max_length=10)