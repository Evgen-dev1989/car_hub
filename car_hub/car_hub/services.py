from car .models import Category, Car

# passenger_car = Category.objects.create(name = 'passenger car')
# cargo_car = Category.objects.create(name = 'cargo car')

# sedan = Category.objects.create(name="Седаны", parent=passenger_car)
# crossover = Category.objects.create(name="Кроссоверы", parent=passenger_car)
# fura = Category.objects.create(name="Фуры", parent=cargo_car)
# pickup = Category.objects.create(name="Пикапы", parent=cargo_car)

def get_categories():
    categories = Category.objects.filter(parent__isnull=True).order_by('parent')  # get only top-level categories
    for category in categories:
        return category.name

        # category.subcategories = Category.objects.filter(parent=category).order_by('name')  # get subcategories for current category
        # for subcategory in category.subcategories:
        #     subcategory.subcategories = Category.objects.filter(parent=subcategory).order_by('name')  # get subcategories for current subcategory
    #return [sedan, crossover, fura, pickup]

# def get_cars_by_category(category_name):
#     category = Category.objects.get(name=category_name)
#     cars = Car.objects.filter(category=category)
#     return cars
