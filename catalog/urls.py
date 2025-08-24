from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('contacts/', views.contacts, name='contacts'),
    path('product_catalog/', views.product_catalog, name='product_catalog'),
    path('product/<int:id>', views.product, name='product'),
    path('add_product/', views.add_product, name='add_product'),
]