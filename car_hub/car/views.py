from django.shortcuts import render
from car_hub.services import  get_categories

def cars_page(request):
    return render(request, 'cars.html', {'categories':get_categories(request)})
