from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from .models import Product, Category
from users.models import User
from messanger.models import Message, MessageReceiver


@admin.register(Product)
class Admin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'status', 'owner')
    search_fields = ('name', 'description')
    list_filter = ('category',)


@admin.register(Category)
class Admin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name', 'description')


@admin.register(User)
class Admin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'avatar', 'country')


@admin.register(Message)
class Admin(admin.ModelAdmin):
    list_display = ('subject', 'message')


@admin.register(MessageReceiver)
class Admin(admin.ModelAdmin):
    list_display = ('email', 'fullname', 'comment')
