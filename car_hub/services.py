import os
import sys

import django

sys.stdout.reconfigure(encoding='utf-8')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_hub.settings')
django.setup()
from decimal import Decimal

from car.models import Car, Category
from django.conf import settings


class Cart:
    def __init__(self, request):

        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}  
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

        self.session.modified = True

    def __iter__(self):

        car_ids = self.cart.keys()
        cars = Car.objects.filter(id__in=car_ids)
        for car in cars:
            self.cart[str(car.id)]['car'] = car

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):

        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):

        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
  
        del self.session[settings.CART_SESSION_ID]
        self.save()


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


# passenger_car = Category.objects.create(name = 'passenger car')
# cargo_car = Category.objects.create(name = 'cargo car')

# sedan = Category.objects.create(name="sedan", parent=passenger_car)
# universal = Category.objects.create(name="universal", parent=passenger_car)
# hatchback = Category.objects.create(name="hatchback", parent=passenger_car)
# liftback = Category.objects.create(name="liftback", parent=passenger_car)
# coupe = Category.objects.create(name="coupe", parent=passenger_car)
# cabriolet = Category.objects.create(name="cabriolet", parent=passenger_car)

# pickup = Category.objects.create(name="pickup", parent=cargo_car)
# onboard = Category.objects.create(name="onboard", parent=cargo_car)
# dump_trucks_with_tipping_body = Category.objects.create(name="dump trucks with tipping body", parent=cargo_car)
# dump_trucks_tractors = Category.objects.create(name="dump trucks tractors", parent=cargo_car)
# eurotruck = Category.objects.create(name="eurotruck", parent=cargo_car)


# Car.objects.create(color="Red", brand="Toyota", model="Camry", year=2022, price=30000.00, category=sedan)
# Car.objects.create(color="Blue", brand="Honda", model="Accord", year=2021, price=28000.00, category=sedan)
# Car.objects.create(color="Black", brand="Hyundai", model="Sonata", year=2023, price=29000.00, category=sedan)

# Car.objects.create(color="White", brand="Volkswagen", model="Passat", year=2020, price=32000.00, category=universal)
# Car.objects.create(color="Gray", brand="Subaru", model="Outback", year=2021, price=35000.00, category=universal)
# Car.objects.create(color="Silver", brand="Audi", model="A4 Avant", year=2022, price=40000.00, category=universal)

# Car.objects.create(color="Yellow", brand="Ford", model="Focus", year=2019, price=22000.00, category=hatchback)
# Car.objects.create(color="Green", brand="Kia", model="Ceed", year=2021, price=23000.00, category=hatchback)
# Car.objects.create(color="Red", brand="Mazda", model="3", year=2022, price=25000.00, category=hatchback)

# Car.objects.create(color="Black", brand="Skoda", model="Octavia", year=2021, price=27000.00, category=liftback)
# Car.objects.create(color="White", brand="Tesla", model="Model S", year=2023, price=80000.00, category=liftback)
# Car.objects.create(color="Blue", brand="BMW", model="4 Series", year=2022, price=50000.00, category=liftback)

# Car.objects.create(color="Red", brand="Chevrolet", model="Camaro", year=2020, price=45000.00, category=coupe)
# Car.objects.create(color="Black", brand="Ford", model="Mustang", year=2021, price=55000.00, category=coupe)
# Car.objects.create(color="White", brand="Nissan", model="370Z", year=2022, price=43000.00, category=coupe)

# Car.objects.create(color="Blue", brand="Porsche", model="911", year=2023, price=120000.00, category=cabriolet)
# Car.objects.create(color="Yellow", brand="Mercedes-Benz", model="E-Class", year=2022, price=70000.00, category=cabriolet)
# Car.objects.create(color="Red", brand="BMW", model="Z4", year=2021, price=65000.00, category=cabriolet)


# Car.objects.create(color="Black", brand="Ford", model="F-150", year=2020, price=40000.00, category=pickup)
# Car.objects.create(color="White", brand="Chevrolet", model="Silverado", year=2021, price=42000.00, category=pickup)
# Car.objects.create(color="Blue", brand="Toyota", model="Hilux", year=2022, price=38000.00, category=pickup)

# Car.objects.create(color="Gray", brand="MAN", model="TGS", year=2019, price=90000.00, category=onboard)
# Car.objects.create(color="White", brand="Volvo", model="FH", year=2021, price=95000.00, category=onboard)
# Car.objects.create(color="Black", brand="Scania", model="R-Series", year=2022, price=100000.00, category=onboard)

# Car.objects.create(color="Yellow", brand="Caterpillar", model="793F", year=2018, price=1500000.00, category=dump_trucks_with_tipping_body)
# Car.objects.create(color="Orange", brand="Komatsu", model="HD785", year=2020, price=1400000.00, category=dump_trucks_with_tipping_body)
# Car.objects.create(color="Gray", brand="BelAZ", model="75710", year=2021, price=3000000.00, category=dump_trucks_with_tipping_body)

# Car.objects.create(color="Black", brand="Kenworth", model="W990", year=2019, price=130000.00, category=dump_trucks_tractors)
# Car.objects.create(color="White", brand="Peterbilt", model="389", year=2021, price=140000.00, category=dump_trucks_tractors)
# Car.objects.create(color="Blue", brand="Freightliner", model="Cascadia", year=2022, price=145000.00, category=dump_trucks_tractors)

# Car.objects.create(color="Gray", brand="DAF", model="XF", year=2020, price=120000.00, category=eurotruck)
# Car.objects.create(color="Black", brand="Renault", model="T High", year=2021, price=125000.00, category=eurotruck)
# Car.objects.create(color="White", brand="Mercedes-Benz", model="Actros", year=2022, price=130000.00, category=eurotruck)
