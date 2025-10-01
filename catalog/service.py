from .models import Product


class ProductService:

    @staticmethod
    def same_category(category):
        return Product.objects.filter(category_id=category)

