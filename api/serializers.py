from rest_framework import serializers, exceptions, status, response
from .models import MedicalCondition, Medication, Nutrients, Allergy, Ingredients, MedicalProfile, MedicalNutrientNeedItem, User, Company, Recipe, Store, StoreItem
from rest_framework_simplejwt.tokens import RefreshToken
class MetricSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()

class AllergySerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergy
        fields = ['id', 'name']

class NutrientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutrients
        fields = ['id', 'name']

class MedicalConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalCondition
        fields = ['id', 'name', 'diagnose_date', 'learn_more', 'explanation']

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = ['id', 'name', 'frequency', 'dosage', 'condition']

class IngredientSerializer(serializers.ModelSerializer):
    allergies = AllergySerializer(many=True)

    class Meta:
        model = Ingredients
        fields = ['id', 'name', 'allergies']

class MedicalProfileSerializer(serializers.ModelSerializer):
    conditions = MedicalConditionSerializer(many=True)
    food_allergies = AllergySerializer(many=True)

    class Meta:
        model = MedicalProfile
        fields = ['id', 'owner_id', 'conditions', 'dietary_highlights', 'summary', 'food_allergies']
        
        exclude = ["owner_id"]

class MedicalNutrientNeedItemSerializer(serializers.ModelSerializer):
    nutrient = NutrientsSerializer(many=True)

    class Meta:
        model = MedicalNutrientNeedItem
        fields = ['id', 'nutrient', 'amount', 'metric']


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ['id', 'cover_photo', 'profile_photo', 'name', 'about', 'joined']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_company',  'account_balance', 'image_url', 'lat', 'long', 'password']
        
        read_only_fields = ['account_balance']
        extra_kwargs = {
            'password': {'write_only': True},  # Exclude password from serialized output
        }
    
    

class RecipeSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'preparation_method', 'ingredients', 'company']


class StoreItemSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        model = StoreItem
        fields = ['id', 'store', 'ingredient', 'date_in', 'amount', 'metric']


class StoreSerializer(serializers.ModelSerializer):
    items = StoreItemSerializer(many=True)
    class Meta:
        model = Store
        fields = ['id', 'last_updated', 'items']

class ProfileSerializer(serializers.Serializer):
    user = UserSerializer()
    medical_profiles = MedicalProfileSerializer()
    
    