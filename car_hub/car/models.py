from client.models import Client
from django.db import models


class Category(models.Model):

    name = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories'
    )

    def __str__(self):

        if self.parent:
            return f"{self.parent.name}"
        else: 
            return f"{self.name}"

class Car(models.Model):

    id = models.AutoField(primary_key=True)
    color = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="cars")
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField(default=2000, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True, related_name="cars")  
    reviews = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"

