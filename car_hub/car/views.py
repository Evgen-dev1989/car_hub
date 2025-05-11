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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from config import email_host_user
from haystack.generic_views import SearchView


class CarSearchView(SearchView):
    template_name = 'search/search.html'
    
def cars_categories_page(request):

    cargo_cars = get_subcategories_cargo() 
    passenger_cars = get_subcategories_passenger() 
    return render(request, 'categories_cars.html', context={'cargo_cars': cargo_cars, 'passenger_cars': passenger_cars})

def category_detail(request, category_id):

    category = get_object_or_404(Category, id=category_id) 
    cars = Car.objects.filter(category=category)
    form = ReviewForm()  
    reviews = Review.objects.filter(car__category=category)
    return render(request, 'category_detail.html', {'category': category, 'cars': cars,'form': form, 'reviews': reviews})



def user_register(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('email') 
            password = form.cleaned_data.get('phone') 


            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
  
                client, created = Client.objects.get_or_create(user=user, defaults={'email': username})
                if created:
                    print(f"Client created: {client.email}")
                else:
                    print(f"The client already exists: {client.email}")
                messages.error(request, "A user with this email is already registered. Please log in..")
                return redirect('login')

            try:
        
                user = User.objects.create_user(username=username, password=password)

       
                client = form.save(commit=False)
                client.user = user
                client.email = username.strip() 
                client.save()

                messages.success(request, "You have registered successfully.")
                return redirect('car')
            except Exception as e:
                messages.error(request, f"An error occurred while registering: {e}")
                return redirect('registr')
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


def cart_send_mail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    cart = Cart(request)
    cart.add(car=car, quantity=1)

    if request.user.is_authenticated:
        try:
            client = Client.objects.get(user=request.user)
            send_mail(
                subject='Purchase Confirmation',
                message=f'Dear {client.user.username},\n\nYou have successfully completed the purchase of "{car.brand} {car.model}" our manager will contact you shortly.\n\nThank you for choosing us!',
                from_email=email_host_user, 
                recipient_list=[client.email], 
                fail_silently=False,
            )
            print("Thank you for your purchase, we sent you an email")
        except Client.DoesNotExist:
            print("Client not found. Email not sent.")
        return redirect('cart_detail', category_id=car.category.id)
    return redirect('category_detail', category_id=car.category.id)

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


from django.contrib.auth.models import AnonymousUser

def reviews_add(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.car = car

            email = request.POST.get('email')

            if not email:
                messages.error(request, "Email not specified. Please enter email.")
                return redirect('category_detail', category_id=car.category.id)


            try:
                client = Client.objects.get(email=email.strip())  
                review.client = client  
            except Client.DoesNotExist:
                messages.error(request, f"Client with email {email} not found. Please register.")
                return redirect('registr')  

            review.save()
            messages.success(request, "Your review has been successfully added.")
            return redirect('category_detail', category_id=car.category.id)
    else:
        form = ReviewForm()


    reviews = Review.objects.filter(car=car)

    return render(request, 'category_detail.html', {
        'form': form,
        'car': car,
        'reviews': reviews
    })


def reviews_show(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    reviews = Review.objects.filter(car=car)
    return render(request, 'category_detail', {'car': car, 'reviews': reviews})

class Car_View(ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
