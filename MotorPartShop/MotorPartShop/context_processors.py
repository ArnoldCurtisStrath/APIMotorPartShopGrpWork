from orders.models import Cart

def cart_context(request):
    cart_item_count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item_count = cart.item_count
        except Cart.DoesNotExist:
            cart_item_count = 0
    return {'cart_item_count': cart_item_count}
