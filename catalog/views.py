from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Category

from django.views.generic import ListView, DetailView, CreateView,TemplateView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy

# Create your views here.


class ProductCatalog(ListView):
    model = Product


class ProductDetail(DetailView):
    model = Product


class ProductCreate(CreateView):
    model = Product
    fields = ['name', 'description', 'image', 'category', 'price']
    success_url = reverse_lazy('catalog:product_list')


class ContactView(TemplateView):
    template_name = 'catalog/contacts.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        return HttpResponse(f"Спасибо за отправку формы {name}!")


class HomeView(TemplateView):
    template_name = 'catalog/home.html'



##def home(request):
##    return render(request, 'catalog/home.html')
##
#
##def contacts(request):
##    if request.method == 'POST':
##        name = request.POST.get('name')
##        phone = request.POST.get('phone')
##        message = request.POST.get('message')
##        return HttpResponse (f'Спасибо за отправку формы {name}')
##    return render(request, 'catalog/contacts.html')
#
#
##def product_catalog(request):
##    products = Product.objects.all()
##    context = {'products': products}
##    return render(request, 'catalog/product_list.html', context)
#
#
##def product(request, id):
##    show_product = Product.objects.get(id=id)
##    context = {'product': show_product}
##    return render(request, 'catalog/product_detail.html', context)
#
#
##def add_product(request):
##    if request.method == 'POST':
##        name = request.POST.get('name')
##        description = request.POST.get('description')
##        image = request.FILES.get('image')
##        category = request.POST.get('category')
##        price = request.POST.get('price')
##        input_product = Product.objects.create(name=name, description=description, image=image,
##                                         category_id=category, price=price)
##        return redirect('catalog:product_catalog')
##    return render(request, 'catalog/product_form.html')