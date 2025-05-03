from django.db import models
from django.contrib.auth.models import User
from car_hub.car.models import Car



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
    
class Payment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, null=True, blank=True, payment_type=[
            ('cash', 'cash'),
            ('Completed', 'Completed'),
            ('Failed', 'Failed')
        ])
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    currency = models.CharField(max_length=10, default='EUR')
    status = models.CharField(max_length=20, default='Pending', choices=[
            ('Pending', 'Pending'),
            ('Completed', 'Completed'),
            ('Failed', 'Failed')
        ])
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)

    
    def send_payment_details(self):
        self.client.user.email_user(
            subject="Payment Details",
            message=f"Payment of {self.amount} {self.currency} was made on {self.payment_date}.",
        )

    def __str__(self):
        return f"Payment {self.id} by {self.client.user_name or self.client.user.username}"