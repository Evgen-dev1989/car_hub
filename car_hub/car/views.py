import os
import sys
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services import get_subcategories_cargo, get_subcategories_passenger, Cart

from .models import Category, Car


def cars_categories_page(request):

    cargo_cars = get_subcategories_cargo() 
    passenger_cars = get_subcategories_passenger() 
    return render(request, 'categories_cars.html', context={'cargo_cars': cargo_cars, 'passenger_cars': passenger_cars})

def category_detail(request, category_id):

    category = get_object_or_404(Category, id=category_id) 
    cars = Car.objects.filter(category=category)
    return render(request, 'category_detail.html', {'category': category, 'cars': cars})

def cart_add(request, car_id):

    cart = Cart(request)
    car = get_object_or_404(Car, id=car_id)
    cart.add(car=car)
    return redirect('cart_detail')

def cart_delete(request, car_id):
  
    cart = Cart(request)
    car = get_object_or_404(Car, id=car_id)
    cart.remove(car)
    return redirect('cart_detail')

def cart_view(request):

    cart = Cart(request)
    return render(request, 'cart.html', {'cart': cart})

