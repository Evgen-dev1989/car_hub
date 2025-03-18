from car .models import Category, Car

# passenger_car = Category.objects.create(name = 'passenger car')
# cargo_car = Category.objects.create(name = 'cargo car')

# sedan = Category.objects.create(name="Седаны", parent=passenger_car)
# crossover = Category.objects.create(name="Кроссоверы", parent=passenger_car)
# fura = Category.objects.create(name="Фуры", parent=cargo_car)
# pickup = Category.objects.create(name="Пикапы", parent=cargo_car)

def get_categories():
    m = Category.objects.filter(parent__isnull=True).order_by('parent')  # get only top-level categories
   
    return m
    #return [sedan, crossover, fura, pickup]
get_categories()