import copy
import os
import sys
from decimal import Decimal
from django.db import models
import django
from car.models import Car, Cart_Model, Category, Review
from client.models import Client
from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib.syndication.views import Feed
from django.urls import path
from car.models import Car
from django.contrib.sitemaps import Sitemap

    

class CarSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Car.objects.all().order_by('id')
    
    def __call__(self, request, *args, **kwargs):
        response = super().__call__(request, *args, **kwargs)
        response.content = b'<?xml-stylesheet type="text/xsl" href="/static/sitemap-stylesheet.xsl"?>\n' + response.content
        return response

    
class LatestCarsFeed(Feed):
    title = "Latest Cars"
    link = "/rss/"
    description = "Updates on the latest cars available."

    def items(self):
        return Car.objects.order_by('-id')[:5] 

    def item_title(self, item):
        return f"{item.brand} {item.model}"

    def item_description(self, item):
        return f"Year: {item.year}, Price: {item.price} ₽"
    
    def __call__(self, request, *args, **kwargs):
  
        response = super().__call__(request, *args, **kwargs)
        response.content = b'<?xml-stylesheet type="text/xsl" href="/static/rss-stylesheet.xsl"?>\n' + response.content
        return response

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['phone', 'email', 'birth_date', 'address', 'city', 'country']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class ReviewForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Ваш email") 

    class Meta:
        model = Review
        fields = ['text'] 
        widgets = {
            'text': forms.Textarea(attrs={
                'placeholder': 'Напишите ваш отзыв',
                'rows': 3,
                'class': 'form-control'
            }),
        }

class Cart:
    def __init__(self, request):
        self.session = request.session
        self.user = request.user if request.user.is_authenticated else None
        self.client = None

        if self.user:
            try:
                self.client = self.user.client
            except Client.DoesNotExist:
                self.client = Client.objects.create(
                    user=self.user,
                    first_name=self.user.username,
                    last_name="Unknown",
                    phone=f"123456789{self.user.id}",
                    email=f"{self.user.username}@example.com"
                )

        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        if self.client:
            try:
                cart_model = self.client.cart
                cart = cart_model.data
                self.session[settings.CART_SESSION_ID] = cart
            except Cart_Model.DoesNotExist:
                cart_model = Cart_Model.objects.create(client=self.client, data=cart)

        self.cart = cart

    def add(self, car, quantity=1, update_quantity=False):
        car_id = str(car.id)
        if car_id not in self.cart:
            self.cart[car_id] = {'quantity': 0, 'price': str(car.price)}
        if update_quantity:
            self.cart[car_id]['quantity'] = quantity
        else:
            self.cart[car_id]['quantity'] += quantity
        self.save()

    def remove(self, car):
        car_id = str(car.id)
        if car_id in self.cart:
            del self.cart[car_id]
            self.save()

    def save(self):
        serialized_cart = {}
        for car_id, item in self.cart.items():
            serialized_cart[car_id] = {
                'quantity': item['quantity'],
                'price': str(item.get('price', '0'))
            }

        if self.client:
            Cart_Model.objects.update_or_create(
                client=self.client,
                defaults={"data": serialized_cart}
            )

        self.session[settings.CART_SESSION_ID] = serialized_cart
        self.session.modified = True
        self.cart = serialized_cart

    def __iter__(self):
        cart_copy = copy.deepcopy(self.cart)
        car_ids = cart_copy.keys()
        cars = Car.objects.filter(id__in=car_ids)

        for car in cars:
            cart_copy[str(car.id)]['car'] = car

        for item in cart_copy.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        if self.client:
            try:
                cart_model = self.client.cart
                cart_model.data = {}
                cart_model.save()
            except Cart_Model.DoesNotExist:
                pass
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True

class CustomLoginView(auth_views.LoginView):
    template_name = 'categories_cars.html' 
    redirect_authenticated_user = True  
    next_page = reverse_lazy('car')  

    def form_valid(self, form):

        user = form.get_user()
        if not Client.objects.filter(user=user).exists():
 
            return redirect('registr')
        return super().form_valid(form)

def get_subcategories_passenger():
    passenger_car = Category.objects.filter(name="passenger car").first()  
    if passenger_car:
        return passenger_car.subcategories.all() 
    return []

def get_subcategories_cargo():
    cargo_car = Category.objects.filter(name="cargo car").first()  
    if cargo_car:
        return cargo_car.subcategories.all() 
    return []



@receiver(post_save, sender=User)
def create_client(sender, instance, created, **kwargs):
    print("create_client signal triggered")
    if not hasattr(instance, 'client'):
  
        Client.objects.create(
            user=instance,
            phone=f"123456789{instance.id}",
            email=instance.username 
        )

@receiver(post_save, sender=User)
def save_client(sender, instance, **kwargs):
    print("save_client signal triggered")
    if hasattr(instance, 'client'):
        instance.client.save()

@receiver(post_save, sender=Client)
def create_cart(sender, instance, created, **kwargs):
    print("create_cart signal triggered")
    if not hasattr(instance, 'cart'):

        Cart_Model.objects.create(client=instance, data={})

# cd /home/camkaenota/solr-9.8.1
#bin/solr start --host 0.0.0.0 --port 8983 --user-managed
#bin/solr stop -p 8983
#bin/solr restart

# python manage.py clear_index --noinput
# python manage.py rebuild_index

# Remove-Item car/migrations/* -Exclude __init__.py -Force
# Remove-Item db.sqlite3 -Force
# python manage.py makemigrations car
# python manage.py migrate
# python manage.py runserver


passenger_car, _ = Category.objects.get_or_create(name = 'passenger car')
cargo_car, _  = Category.objects.get_or_create(name = 'cargo car')

sedan, _  = Category.objects.get_or_create(name="sedan", parent=passenger_car)
universal, _  = Category.objects.get_or_create(name="universal", parent=passenger_car)
hatchback, _  = Category.objects.get_or_create(name="hatchback", parent=passenger_car)
liftback, _  = Category.objects.get_or_create(name="liftback", parent=passenger_car)
coupe, _  = Category.objects.get_or_create(name="coupe", parent=passenger_car)
cabriolet, _  = Category.objects.get_or_create(name="cabriolet", parent=passenger_car)

pickup, _  = Category.objects.get_or_create(name="pickup", parent=cargo_car)
onboard, _  = Category.objects.get_or_create(name="onboard", parent=cargo_car)
dump_trucks_with_tipping_body, _  = Category.objects.get_or_create(name="dump trucks with tipping body", parent=cargo_car)
dump_trucks_tractors, _  = Category.objects.get_or_create(name="dump trucks tractors", parent=cargo_car)
eurotruck, _  = Category.objects.get_or_create(name="eurotruck", parent=cargo_car)


Car.objects.get_or_create(color="Red", brand="Toyota", model="Camry", year=2022, price=30000.00, category=sedan)
Car.objects.get_or_create(color="Blue", brand="Honda", model="Accord", year=2021, price=28000.00, category=sedan)
Car.objects.get_or_create(color="Black", brand="Hyundai", model="Sonata", year=2023, price=29000.00, category=sedan)

Car.objects.get_or_create(color="White", brand="Volkswagen", model="Passat", year=2020, price=32000.00, category=universal)
Car.objects.get_or_create(color="Gray", brand="Subaru", model="Outback", year=2021, price=35000.00, category=universal)
Car.objects.get_or_create(color="Silver", brand="Audi", model="A4 Avant", year=2022, price=40000.00, category=universal)

Car.objects.get_or_create(color="Yellow", brand="Ford", model="Focus", year=2019, price=22000.00, category=hatchback)
Car.objects.get_or_create(color="Green", brand="Kia", model="Ceed", year=2021, price=23000.00, category=hatchback)
Car.objects.get_or_create(color="Red", brand="Mazda", model="3", year=2022, price=25000.00, category=hatchback)

Car.objects.get_or_create(color="Black", brand="Skoda", model="Octavia", year=2021, price=27000.00, category=liftback)
Car.objects.get_or_create(color="White", brand="Tesla", model="Model S", year=2023, price=80000.00, category=liftback)
Car.objects.get_or_create(color="Blue", brand="BMW", model="4 Series", year=2022, price=50000.00, category=liftback)

Car.objects.get_or_create(color="Red", brand="Chevrolet", model="Camaro", year=2020, price=45000.00, category=coupe)
Car.objects.get_or_create(color="Black", brand="Ford", model="Mustang", year=2021, price=55000.00, category=coupe)
Car.objects.create(color="White", brand="Nissan", model="370Z", year=2022, price=43000.00, category=coupe)

Car.objects.get_or_create(color="Blue", brand="Porsche", model="911", year=2023, price=120000.00, category=cabriolet)
Car.objects.get_or_create(color="Yellow", brand="Mercedes-Benz", model="E-Class", year=2022, price=70000.00, category=cabriolet)
Car.objects.get_or_create(color="Red", brand="BMW", model="Z4", year=2021, price=65000.00, category=cabriolet)


Car.objects.get_or_create(color="Black", brand="Ford", model="F-150", year=2020, price=40000.00, category=pickup)
Car.objects.get_or_create(color="White", brand="Chevrolet", model="Silverado", year=2021, price=42000.00, category=pickup)
Car.objects.get_or_create(color="Blue", brand="Toyota", model="Hilux", year=2022, price=38000.00, category=pickup)

Car.objects.get_or_create(color="Gray", brand="MAN", model="TGS", year=2019, price=90000.00, category=onboard)
Car.objects.get_or_create(color="White", brand="Volvo", model="FH", year=2021, price=95000.00, category=onboard)
Car.objects.get_or_create(color="Black", brand="Scania", model="R-Series", year=2022, price=100000.00, category=onboard)

Car.objects.get_or_create(color="Yellow", brand="Caterpillar", model="793F", year=2018, price=1500000.00, category=dump_trucks_with_tipping_body)
Car.objects.get_or_create(color="Orange", brand="Komatsu", model="HD785", year=2020, price=1400000.00, category=dump_trucks_with_tipping_body)
Car.objects.get_or_create(color="Gray", brand="BelAZ", model="75710", year=2021, price=3000000.00, category=dump_trucks_with_tipping_body)

Car.objects.get_or_create(color="Black", brand="Kenworth", model="W990", year=2019, price=130000.00, category=dump_trucks_tractors)
Car.objects.get_or_create(color="White", brand="Peterbilt", model="389", year=2021, price=140000.00, category=dump_trucks_tractors)
Car.objects.get_or_create(color="Blue", brand="Freightliner", model="Cascadia", year=2022, price=145000.00, category=dump_trucks_tractors)

Car.objects.get_or_create(color="Gray", brand="DAF", model="XF", year=2020, price=120000.00, category=eurotruck)
Car.objects.get_or_create(color="Black", brand="Renault", model="T High", year=2021, price=125000.00, category=eurotruck)
Car.objects.get_or_create(color="White", brand="Mercedes-Benz", model="Actros", year=2022, price=130000.00, category=eurotruck)

# Category.objects.all().delete()
# Car.objects.all().delete()
