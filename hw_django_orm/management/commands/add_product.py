from django.core.management.base import BaseCommand
from hw_django_orm.models import Product, Category
from django.db import connection
import json


class Command(BaseCommand):

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE hw_django_orm_product RESTART IDENTITY;')
            cursor.execute('TRUNCATE TABLE hw_django_orm_category RESTART IDENTITY CASCADE;')

        with open('hw_django_orm_fixture.json', 'r', encoding='UTF-8') as file:
            item_data = json.load(file)

            for data in item_data:
                if data['model'] == 'hw_django_orm.category':
                    category = Category.objects.create(**data['fields'])
                    self.stdout.write(self.style.SUCCESS(f'Добавлен продукт: {category.name}'))

            for data in item_data:
                if data['model'] == 'hw_django_orm.product':
                    data['fields']['category_id'] = data['fields'].pop('category')
                    product = Product.objects.create(**data['fields'])
                    self.stdout.write(self.style.SUCCESS(f'Добавлен продукт: {product.name}'))
