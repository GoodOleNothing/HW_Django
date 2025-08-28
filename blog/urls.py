from django.urls import path
from .views import BlogView

app_name = 'blog'

urlpatterns = [
    path('blog_list/', BlogView.as_view(), name='blog_list'),
]