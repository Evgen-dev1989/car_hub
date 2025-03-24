from car.views import cars_categories_page, category_detail
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('client/', include('client.urls')),
    path('car/', cars_categories_page),
    path('car/<int:category_id>/', category_detail, name='category_detail')
]
