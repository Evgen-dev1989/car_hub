from django.db import models
from django.contrib.auth.models import User



class Client(models.Model):
    user = models.OneToOneField(
        'auth.User',
        on_delete=models.CASCADE,
        related_name="client",
        null=True, 
        blank=True 
    )
    user_name = models.CharField(max_length=150, unique=True, null=True, blank=True)  # Добавлено поле
    phone = models.CharField(max_length=15, unique=True, null=True)
    email = models.EmailField(max_length=100, unique=True, null=True)
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

    def __str__(self):
        return f"{self.user_name or self.user.username}" 