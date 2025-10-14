from django.db import models
from django.conf import settings


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Имя')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    image = models.ImageField(blank=True, default=None, upload_to='product_image/', verbose_name='Изображение')
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, related_name='Кат')
    price = models.IntegerField(verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    status = models.BooleanField(default=True, verbose_name='Активен')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='Владелец',
                              null=True, blank=True)

    def __str__(self):
        return f'{self.name}, {self.category}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['id']
        permissions = (
            ("can_unpublish_product", "Can unpublish product"),
            ("can_change_product_price", "Can change product price"),
            ("can_change_product_description", "Can change product description"),
        )


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Категория')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категоря'
        verbose_name_plural = 'Категории'
        ordering = ['id']
