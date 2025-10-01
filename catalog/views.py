from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from .models import Product, Category
from django.views.generic import ListView, DetailView, CreateView,TemplateView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django import forms
from .models import Product, Category
from .forms import ProductForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .service import ProductService
# Create your views here.


class SameCategryView(ListView):
    model = Product
    template_name = 'catalog/same_category_list.html'

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        return ProductService.same_category(category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_manager'] = self.request.user.groups.filter(name="Product Manager").exists()
        context['categories'] = Category.objects.all()
        return context


class ProductCatalog(ListView):
    model = Product

    def get_queryset(self):
        data = cache.get('product_list')
        if not data:
            data = Product.objects.all()
            cache.set('product_list', data, 60 * 15)
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_manager'] = self.request.user.groups.filter(name="Product Manager").exists()
        context['categories'] = Category.objects.all()
        return context



@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetail(DetailView):
    model = Product


class ProductCreate(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        default_status = Product._meta.get_field('status').default
        if form.instance.status != default_status: # статус не по умолчанию
            if not self.request.user.has_perm("catalog.can_unpublish_product") and not self.request.user.groups.filter(name="Product Manager").exists():
                return HttpResponseForbidden("Вы не модератор. У вас нет права активироавать/деактивировать товар")
        return super().form_valid(form)


class ProductDelete(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:product_list')

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        if product.owner != request.user and not request.user.groups.filter(name="Product Manager").exists():
            if not self.request.user.has_perm("catalog.can_delete_product"):
                return HttpResponseForbidden("Вы не владелец и не модератор. У вас нет прав на удаление этого товара")

        return super().dispatch(request, *args, **kwargs)


class ProductUpdate(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_update.html'
    success_url = reverse_lazy('catalog:product_list')

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        if product.owner != request.user and not request.user.groups.filter(name="Product Manager").exists():
            return HttpResponseForbidden("Вы не владелец и не модератор. У вас нет прав на редактирование этого товара")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        product = self.get_object()
        if form.cleaned_data.get("status") != product.status:
            if not self.request.user.has_perm("catalog.can_unpublish_product") and not self.request.user.groups.filter(name="Product Manager").exists():
                return HttpResponseForbidden("Вы не модератор. У вас нет права активироавать/деактивировать товар")

        return super().form_valid(form)


#class ProductCreate(CreateView):
#    model = Product
#    fields = ['name', 'description', 'image', 'category', 'price']
#    success_url = reverse_lazy('catalog:product_list')


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