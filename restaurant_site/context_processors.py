from .views import AddToCart, ProductPhotos
from django.http import HttpResponseRedirect


def custom_data(request):
    if request.user.is_authenticated:
        cart_products = AddToCart.objects.filter(customer=request.user)
        number_of_products = len(cart_products)
        menu_products = ProductPhotos.objects.filter(pro_id__category='pizza')[:6]
        total_price = 0
        for product in cart_products:
            total_price += (product.product.price * product.quantity)
        context = {
            'cart_products': cart_products,
            'items': number_of_products,
            'total_price': total_price,
            'menu_products': menu_products,
        }

        return context
    else:
        cart_products = []
        number_of_products = 0
        total_price = 0
        menu_products = ProductPhotos.objects.filter(pro_id__category='pizza')[:6]
        context = {
            'cart_products': cart_products,
            'items': number_of_products,
            'total_price': total_price,
            'menu_products': menu_products,
        }
        return context
