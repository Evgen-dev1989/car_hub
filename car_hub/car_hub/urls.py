from car.views import (Car_View, CarSearchView, car_detail,
                       cars_categories_page, cart_add, cart_clear, cart_delete,
                       cart_send_mail, cart_view, category_detail,
                       placing_order, reviews_add, user_register)
from client.views import all_clients, delete_all_users
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import SimpleRouter
from services import CarSitemap, CustomLoginView, LatestCarsFeed

router = SimpleRouter()
router.register('api/cars', Car_View, basename='car')

sitemaps = {
    'cars': CarSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('client/', include('client.urls')),
    path('car/', cars_categories_page, name='car'),
    path('car/register/', user_register, name='user_register'),
    path('car/<int:pk>/', car_detail, name='car_detail'), 
    path('category/<int:category_id>/', category_detail, name='category_detail'),
    path('add/<int:car_id>/', cart_add, name='cart_add'),
    path('remove/<int:car_id>/', cart_delete, name='cart_remove'),
    path('cart/', cart_view, name='cart_detail'),
    path('cart/<int:car_id>/placing-order/', placing_order, name='placing_order'),
    path('cart/<int:car_id>/send_mail/', cart_send_mail, name='cart_send_mail'),
    path('clear/', cart_clear, name='cart_clear'),
    path('api-auth/', include('rest_framework.urls')),
    path('contacts/', TemplateView.as_view(template_name='contacts.html'), name='contacts'),
    path('delete_users/', delete_all_users, name='delete'),
    path('clients/',  all_clients, name='all_clients'),
    path('car/<int:car_id>/reviews/add/', reviews_add, name='reviews_add'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('rss/', LatestCarsFeed(), name='rss_feed'),
    path('search/', CarSearchView.as_view(), name='haystack_search'),
    path('logout/', LogoutView.as_view(next_page='car'), name='logout'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
urlpatterns += router.urls




