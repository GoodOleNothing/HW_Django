from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView,TemplateView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Blog

# Create your views here.


class BlogView(ListView):
    model = Blog
