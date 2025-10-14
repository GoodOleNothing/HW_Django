from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from .models import Product, Category
from users.models import User
from messanger.models import Message, Recipient, Mailing, AttemptedMailing


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
    list_display = ('id','email', 'phone', 'avatar', 'country', 'is_active')


@admin.register(Message)
class Admin(admin.ModelAdmin):
    list_display = ('subject', 'message')


@admin.register(Recipient)
class Admin(admin.ModelAdmin):
    list_display = ('email', 'fullname', 'comment', 'owner')


@admin.register(Mailing)
class Mailing(admin.ModelAdmin):
    list_display = ('id', 'owner', 'start_time', 'end_time', 'status', 'message')


@admin.register(AttemptedMailing)
class AttemptedMailing(admin.ModelAdmin):
    list_display = ('attempted_at', 'status', 'mail_server_response', 'mailing')
