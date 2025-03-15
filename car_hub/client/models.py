from django.db import models

class Client(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, default="Netherlands")
    passport_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    tax_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    preferred_car_brand = models.CharField(max_length=50, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    