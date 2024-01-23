from rest_framework import serializers
from store.models import Products

class ProductsSerializers (serializers.ModelSerializer): 
    class Meta:
        model = Products
        fields = '__all__'
        