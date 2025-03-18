from django.shortcuts import render
from car_hub.services import  get_categories

def cars_page(request):
    categories = get_categories() 
    return render(request, 'cars.html', context={'categories': categories})
