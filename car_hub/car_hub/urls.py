from django.contrib import admin
from django.urls import path
from car.views import cars_page
urlpatterns = [
    path('admin/', admin.site.urls),
    #path('client/', include('client.urls')),
    path('car/', cars_page)
]
