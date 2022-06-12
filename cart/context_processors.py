from cart.views import _get_cart_id
from core.models import Cart, CartItem


def counter(request):
    if 'admin' in request.path:
        return {}
    try:
        cart = Cart.objects.get(cart_id=_get_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        cart_count = sum(item.quantity for item in cart_items)
    except Cart.DoesNotExist:
        cart_count = 0
    return {'counter': cart_count}
