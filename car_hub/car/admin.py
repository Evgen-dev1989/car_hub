from django.contrib import admin

from .models import Car, Category

admin.site.register(Car)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    
    list_display = ("name", "parent")
    list_filter = ("parent",)