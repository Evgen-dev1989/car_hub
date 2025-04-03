from rest_framework import serializers
from .models import Car

class VarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car