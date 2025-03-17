from car .models import Category

# passenger_car = Category.objects.create(name = 'passenger car')
# cargo_car = Category.objects.create(name = 'cargo car')

# sedan = Category.objects.create(name="Седаны", parent=passenger_car)
# crossover = Category.objects.create(name="Кроссоверы", parent=passenger_car)
# fura = Category.objects.create(name="Фуры", parent=cargo_car)
# pickup = Category.objects.create(name="Пикапы", parent=cargo_car)

def get_categories():
    return Category.objects.all()

print(get_categories())