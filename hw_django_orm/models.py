from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Имя')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    image = models.ImageField(blank=True, default=None, upload_to='product_image/', verbose_name='Изображение')
    category = models.ForeignKey(to='Category',on_delete=models.CASCADE, related_name='Кат')
    price = models.IntegerField(verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    def __str__(self):
        return f'{self.name}, {self.category}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['id']


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Категория')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категоря'
        verbose_name_plural = 'Категории'
        ordering = ['id']
