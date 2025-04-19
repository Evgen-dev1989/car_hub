import os
import sys
from django.shortcuts import get_object_or_404, render, redirect
from rest_framework.viewsets import ModelViewSet
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services import get_subcategories_cargo, get_subcategories_passenger, Cart
from api.serializers_car import CarSerializer
from .models import Category, Car, Review
from client.models import Client
from django.contrib.auth.models import User
from django.contrib import messages

def cars_categories_page(request):

    cargo_cars = get_subcategories_cargo() 
    passenger_cars = get_subcategories_passenger() 
    return render(request, 'categories_cars.html', context={'cargo_cars': cargo_cars, 'passenger_cars': passenger_cars})

def category_detail(request, category_id):

    category = get_object_or_404(Category, id=category_id) 
    cars = Car.objects.filter(category=category)
    return render(request, 'category_detail.html', {'category': category, 'cars': cars})





from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from client.models import Client

def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        birth_date = request.POST.get('birth_date')
        address = request.POST.get('address')
        city = request.POST.get('city')
        country = request.POST.get('country', 'Netherlands')  # Значение по умолчанию
        passport_number = request.POST.get('passport_number')
        tax_id = request.POST.get('tax_id')
        preferred_car_brand = request.POST.get('preferred_car_brand')
        notes = request.POST.get('notes')

        if username and email and password and first_name and last_name and phone:
            user = User.objects.create_user(username=username, email=email, password=password)
            Client.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email,
                birth_date=birth_date,
                address=address,
                city=city,
                country=country,
                passport_number=passport_number,
                tax_id=tax_id,
                preferred_car_brand=preferred_car_brand,
                notes=notes
            )
            messages.add_message(request, messages.SUCCESS, "Аккаунт создан. Войдите в систему.", extra_tags="register")
            return redirect('login-register')
        else:
            messages.add_message(request, messages.WARNING, "Пожалуйста, заполните все обязательные поля.", extra_tags="register")
    return render(request, 'registration.html')


def cart_add(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    cart = Cart(request)
    cart.add(car=car, quantity=1)
    if  car.category:
        category_id = car.category.id
    else:
        category_id = 1 

    return redirect('category_detail', category_id=category_id)


# def cart_add(request, car_id):
#     cart = Cart(request)
#     car = get_object_or_404(Car, id=car_id)
#     cart.add(car=car)

#     if  car.category:
#         category_id = car.category.id
#     else:
#         category_id = 1 

#     return redirect('category_detail', category_id=category_id)

def cart_delete(request, car_id):
  
    cart = Cart(request)
    car = get_object_or_404(Car, id=car_id)
    cart.remove(car)
    return redirect('cart_detail')

def cart_view(request):

    cart = Cart(request)
    return render(request, 'cart.html', {'cart': cart})

def cart_clear(request):
    
    cart = Cart(request)
    cart.clear()
    return redirect('cart_detail')

def reviews_add(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == "POST":
        text = request.POST.get("text")
        client = request.user.client 
        
        if text and client:
            Review.objects.create(car=car, client=client, text=text)

    return redirect('car_detail', car_id=car.id)

class Car_View(ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
