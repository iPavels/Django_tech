from django.core.cache import cache

from .models import Product


CATEGORY_CACHE_TTL = 60


def get_products_by_category(category_id):
    cache_key = f"category_{category_id}"

    products = cache.get(cache_key)

    if products is None:
        products = list(
            Product.objects.filter(category_id=category_id)
        )
        cache.set(cache_key, products, CATEGORY_CACHE_TTL)

    return products
