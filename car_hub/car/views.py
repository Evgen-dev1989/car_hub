import os
import sys
from django.shortcuts import get_object_or_404, render, redirect
from rest_framework.viewsets import ModelViewSet
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services import get_subcategories_cargo, get_subcategories_passenger, Cart, ClientForm
from api.serializers_car import CarSerializer
from .models import Category, Car, Review
from client.models import Client
from django.contrib.auth.models import User
from django.contrib import messages
from services import ReviewForm


def cars_categories_page(request):

    cargo_cars = get_subcategories_cargo() 
    passenger_cars = get_subcategories_passenger() 
    return render(request, 'categories_cars.html', context={'cargo_cars': cargo_cars, 'passenger_cars': passenger_cars})

def category_detail(request, category_id):

    category = get_object_or_404(Category, id=category_id) 
    cars = Car.objects.filter(category=category)
    form = ReviewForm()  
    return render(request, 'category_detail.html', {'category': category, 'cars': cars,'form': form})


def user_register(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data.get('email') 
            password = form.cleaned_data.get('phone') 
            
            if User.objects.filter(username=username).exists():
                messages.error(request, "you are already registered.")
                return redirect('car2')


            user = User.objects.create_user(username=username, password=password)
            client, created = Client.objects.get_or_create(user=user)
            if not created:
                messages.error(request, "Клиент с таким пользователем уже существует.")
                return redirect('car2')
            
            client = form.save(commit=False)
            client.user = user
            client.save()

            messages.success(request, "you have successfully registered")
            return redirect('car') 
    else:
        form = ClientForm()

    return render(request, 'registration.html', {'form': form})



def cart_add(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    cart = Cart(request)
    cart.add(car=car, quantity=1)
    if  car.category:
        category_id = car.category.id
    else:
        category_id = 1 

    return redirect('category_detail', category_id=category_id)



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

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.car = car  
            review.save()
            return render(request, 'category_detail', category_id=car.category.id)
    else:
        form = ReviewForm()

    return render(request, 'category_detail', {'form': form, 'car': car})

def reviews_show(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    reviews = Review.objects.filter(car=car)
    return render(request, 'category_detail', {'car': car, 'reviews': reviews})

class Car_View(ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
