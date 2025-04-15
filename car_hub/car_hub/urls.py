from car.views import cars_categories_page, category_detail, cart_add, cart_view, cart_delete, cart_clear, reviews_add, user_register
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from api.serializers_car import CarSerializer
from car.models import Car
from car.views import Car_View

router = SimpleRouter()
router.register('api/cars', Car_View, basename='car')

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('client/', include('client.urls')),
    path('car/', cars_categories_page, name='car'),
    path('car/<int:category_id>/', category_detail, name='category_detail'),
    path('car/<int:car_id>/add_review/', reviews_add, name='reviews_add'),
    path('add/<int:car_id>/', cart_add, name='cart_add'),
    path('remove/<int:car_id>/', cart_delete, name='cart_remove'),
    path('cart/', cart_view, name='cart_detail'),
    path('clear/', cart_clear, name='cart_clear'),
    path('api-auth/', include('rest_framework.urls')),
    path('registr/', user_register, name='registr'),
]
urlpatterns += router.urls