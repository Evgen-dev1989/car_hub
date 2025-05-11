from car.views import cars_categories_page, category_detail, cart_add, cart_view, cart_delete, cart_clear, reviews_add, user_register, cart_send_mail, reviews_show
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from api.serializers_car import CarSerializer
from car.models import Car
from car.views import Car_View
from client.views import delete_all_users,  all_clients
from services import CustomLoginView, LatestCarsFeed, CarSitemap
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from car.views import CarSearchView


router = SimpleRouter()
router.register('api/cars', Car_View, basename='car')

sitemaps = {
    'cars': CarSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('client/', include('client.urls')),
    path('car/', cars_categories_page, name='car'),
    path('car/', user_register, name='car2'),
    path('car/<int:category_id>/', category_detail, name='category_detail'),
    path('add/<int:car_id>/', cart_add, name='cart_add'),
    path('remove/<int:car_id>/', cart_delete, name='cart_remove'),
    path('cart/', cart_view, name='cart_detail'),
    path('cart/<int:car_id>/send_mail/', cart_send_mail, name='cart_send_mail'),
    path('clear/', cart_clear, name='cart_clear'),
    path('api-auth/', include('rest_framework.urls')),
    path('registr/', user_register, name='registr'),
    path('contacts/', TemplateView.as_view(template_name='Сontacts.html'), name='contacts'),
    path('delete_users/', delete_all_users, name='delete'),
    path('clients/',  all_clients, name='all_clients'),
    path('car/<int:car_id>/reviews/add/', reviews_add, name='reviews_add'),
    path('car/<int:car_id>/reviews/', reviews_show, name='reviews_show'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('rss/', LatestCarsFeed(), name='rss_feed'),
    path('search/', CarSearchView.as_view(), name='haystack_search'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
urlpatterns += router.urls



