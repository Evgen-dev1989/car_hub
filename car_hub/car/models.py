from client.models import Client
from django.db import models
from django.contrib.syndication.views import Feed
from django.urls import reverse
from django import forms
from django.utils.translation import gettext as _
class Category(models.Model):

    name = models.CharField(max_length=50, unique=True, verbose_name=_("Name"))
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories'
    )

    def __str__(self):
        return self.name

class Car(models.Model):

    id = models.AutoField(primary_key=True)
    color = models.CharField(max_length=50, verbose_name=_("Name"))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="cars", verbose_name=_("Name"))
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField(default=2000, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True, related_name="cars")

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"
    
    def get_absolute_url(self):
        return reverse('car_detail', args=[self.id]) #, self.category.id
    

class Review(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="reviews", verbose_name=_("Name"))
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="reviews", null=True, blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

def __str__(self):
    return f"Review by {self.client.first_name} {self.client.last_name} on {self.car.brand} {self.car.model}"

class Cart_Model(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name="cart", verbose_name=_("Name"))

    data = models.JSONField(default=dict)

class Payment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='payments', verbose_name=_("Name"))
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, null=True, blank=True, choices=[
            ('cash', 'cash'),
            ('cashless payment', 'cashless payment'),
            ('bank transfer', 'bank transfer'),
            ('credit card', 'credit card'),
            ('debit card', 'debit card'),
            ('mobile payment', 'mobile payment'),
            ('cryptocurrency', 'cryptocurrency')
        ])
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    currency = models.CharField(max_length=10, default='EUR')
    status = models.CharField(max_length=20, default='Pending', choices=[
            ('Pending', 'Pending'),
            ('Completed', 'Completed'),
            ('Failed', 'Failed')
        ])
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)




    def remove(self, car):
        car_id = str(car.id)
        if car_id in self.car:
            del self.car[car_id]

    
    def send_payment_details(self):
        self.client.user.email_user(
            subject="Payment Details",
            message=f"Payment of {self.amount} {self.currency} was made on {self.payment_date}.",
        )
    
    def __str__(self):
        return f"Payment {self.id} by {self.client.user_name or self.client.user.username}"

class PaymentForm(forms.ModelForm):
    class Meta:
        name = forms.CharField(label=_("Name"))
        model = Payment
        fields = ['payment_method']