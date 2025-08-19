from django.contrib import admin

# Register your models here.
from .models import Product, Category


@admin.register(Product)
class Admin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')
    search_fields = ('name', 'description')
    list_filter = ('category',)


@admin.register(Category)
class Admin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name', 'description')
