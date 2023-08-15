from .models import FavoriteProduct, Notification

def notify_discounts():
    favorite_products = FavoriteProduct.objects.filter(product__discount_price__isnull=False)

    for favorite in favorite_products:
        user = favorite.user
        product = favorite.product

        if not Notification.objects.filter(user=user, message=f"Discount available for {product.name}").exists():
            notification = Notification.objects.create(
                user=user,
                message=f"Discount available for {product.name}: Now at a discounted price of {product.discount_price}!"
            )