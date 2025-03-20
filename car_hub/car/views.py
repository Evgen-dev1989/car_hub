import os
import sys

from django.shortcuts import render

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services import get_categories


def cars_page(request):
    categories = get_categories() 
    return render(request, 'cars.html', context={'categories': categories})
