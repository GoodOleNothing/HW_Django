from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('contacts/', views.ContactView.as_view(), name='contacts'),
    path('product_list/', views.ProductCatalog.as_view(), name='product_list'),
    path('product_detail/<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
    path('add_product/', views.ProductCreate.as_view(), name='add_product'),

   #path('home/', views.home, name='home'),
   #path('contacts/', views.contacts, name='contacts'),
   #path('product_catalog/', views.product_catalog, name='product_catalog'),
   #path('product/<int:id>/', views.product, name='product'),
   #path('add_product/', views.add_product, name='add_product'),
]