from car.views import cars_categories_page, category_detail, cart_add, cart_view, cart_delete, cart_clear
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('client/', include('client.urls')),
    path('car/', cars_categories_page, name='car'),
    path('car/<int:category_id>/', category_detail, name='category_detail'),
    path('add/<int:car_id>/', cart_add, name='cart_add'),
    path('remove/<int:car_id>/', cart_delete, name='cart_remove'),
    path('cart/', cart_view, name='cart_detail'),
    path('clear/', cart_clear, name='cart_clear'),
]
