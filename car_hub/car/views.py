import os
import sys
from django.shortcuts import get_object_or_404, render, redirect
from rest_framework.viewsets import ModelViewSet
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services import get_subcategories_cargo, get_subcategories_passenger, Cart, ClientForm
from api.serializers_car import CarSerializer
from .models import Category, Car, Review, PaymentForm
from client.models import Client
from django.contrib.auth.models import User
from django.contrib import messages
from services import ReviewForm
from django.core.mail import send_mail
from config import email_host_user
from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet
import uuid
from django.contrib.auth import login

class CarSearchView(SearchView):
    template_name = 'search/search.html'
    queryset = SearchQuerySet().all()
    context_object_name = 'object_list'
    paginate_by = 20 

def cars_categories_page(request):

    cargo_cars = get_subcategories_cargo() 
    passenger_cars = get_subcategories_passenger() 
    return render(request, 'categories_cars.html', context={'cargo_cars': cargo_cars, 'passenger_cars': passenger_cars})


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subcategories = category.subcategories.all()
    category_ids = [category.id] + [sub.id for sub in subcategories]
    cars = Car.objects.filter(category_id__in=category_ids)
    form = ReviewForm()
    reviews = Review.objects.filter(car__category__in=category_ids)
    return render(request, 'category_detail.html', {
        'category': category,
        'cars': cars,
        'form': form,
        'reviews': reviews
    })


def car_detail(request, pk):

    car = get_object_or_404(Car, pk=pk)
    category = car.category
    form = ReviewForm()  
    reviews = Review.objects.filter(car=car)
    return render(request, 'result_search_car.html', {'category': category, 'car': car,'form': form, 'reviews': reviews})




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
                login(request, user)
                messages.success(request, "You have registered successfully.")
                return redirect('car')
            except Exception as e:
                messages.error(request, f"An error occurred while registering: {e}")
                return redirect('car_register') 
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


def placing_order(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    cart = Cart(request)


    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to place an order.")
        return redirect('login')

    try:
        client = Client.objects.get(user=request.user)
    except Client.DoesNotExist:
        messages.error(request, "Client not found. Please register.")
        return redirect('user_register')

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.client = client
            payment.amount = car.price
            payment.transaction_id = str(uuid.uuid4())
            payment.currency = 'EUR'
            payment.status = 'Pending'
            payment.car = car
            payment.save()
            messages.success(request, "Order placed successfully!")
            return redirect('cart_detail')
    else:
        form = PaymentForm()

    return render(request, 'placing_order.html', {
        'form': form,
        'cart': cart,
    })


def delete_order(request, car_id):
  
    order = Cart(request)
    car = get_object_or_404(Car, id=car_id)
    order.remove(car)
    return redirect('cart_detail')


def send_order(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    cart = Cart(request)

    if request.user.is_authenticated:
        try:
            client = Client.objects.get(user=request.user)

            send_mail(
                subject='Purchase Confirmation',
                message=(
                    f'Dear {client.user.username},\n\n'
                    f'You have successfully completed the purchase of "{car.brand} {car.model}".\n'
                    f'Total price: {cart.get_total_price(car)}\n'
                    'Our manager will contact you shortly.\n\nThank you for choosing us!'
                ),
                from_email=email_host_user,
                recipient_list=[client.email],
                fail_silently=False,
            )
            print("Thank you for your purchase, we sent you an email")
        except Client.DoesNotExist:
            print("Client not found. Email not sent.")
        return redirect('cart_detail')
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
                return redirect('car_register') 

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


class Car_View(ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
