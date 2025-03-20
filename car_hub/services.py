import os
import django
import sys
sys.stdout.reconfigure(encoding='utf-8')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_hub.settings')
django.setup()
from car.models import Category

passenger_car = Category.objects.create(name = 'passenger car')
cargo_car = Category.objects.create(name = 'cargo car')

sedan = Category.objects.create(name="sedan", parent=passenger_car)
universal = Category.objects.create(name="universal", parent=passenger_car)
hatchback = Category.objects.create(name="hatchback", parent=passenger_car)
liftback = Category.objects.create(name="liftback", parent=passenger_car)
coupe = Category.objects.create(name="coupe", parent=passenger_car)
cabriolet = Category.objects.create(name="cabriolet", parent=passenger_car)

pickup = Category.objects.create(name="pickup", parent=cargo_car)
onboard = Category.objects.create(name="onboard", parent=cargo_car)
dump_trucks_with_tipping_body = Category.objects.create(name="dump trucks with tipping body", parent=cargo_car)
dump_trucks_tractors = Category.objects.create(name="dump trucks tractors", parent=cargo_car)
eurotruck = Category.objects.create(name="eurotruck", parent=cargo_car)

def get_categories():
    categories = Category.objects.filter(parent__isnull=True)  
    result = {}

    for category in categories:
        subcategories = category.subcategories.all() 
        result[category.name] = [sub.name for sub in subcategories]  

    return result
