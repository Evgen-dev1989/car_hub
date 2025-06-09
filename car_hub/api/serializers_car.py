from car.models import Car, Category, Cart_Model, Payment, Review
from client.models import Client
from rest_framework import serializers


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('__all__')

class CartModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart_Model
        fields = ('__all__')

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('__all__')

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('__all__')
        

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ('__all__')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('__all__')

