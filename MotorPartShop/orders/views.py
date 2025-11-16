from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Cart, CartItem, Order, OrderItem
from parts.models import Part

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'orders/cart.html', {'cart': cart})

@login_required
def add_to_cart(request, part_id):
    if request.method == 'POST':
        part = get_object_or_404(Part, pk=part_id)
        quantity = int(request.POST.get('quantity', 1))
        if quantity > part.stock:
            messages.error(request, 'Not enough stock available.')
            return redirect('parts:detail', pk=part_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, part=part)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, f'{part.name} added to cart.')
        return redirect('orders:cart')
    return redirect('parts:list')

@login_required
def update_cart_item(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        if quantity > cart_item.part.stock:
            messages.error(request, 'Not enough stock available.')
        elif quantity <= 0:
            cart_item.delete()
            messages.success(request, 'Item removed from cart.')
        else:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated.')
    return redirect('orders:cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('orders:cart')

@login_required
def clear_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart.items.all().delete()
    messages.success(request, 'Cart cleared.')
    return redirect('orders:cart')

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    
    if not cart.items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('orders:cart')
    
    if request.method == 'POST':
        with transaction.atomic():
            order = Order.objects.create(user=request.user)
            
            for cart_item in cart.items.all():
                if cart_item.quantity > cart_item.part.stock:
                    messages.error(request, f'Not enough stock for {cart_item.part.name}')
                    order.delete()
                    return redirect('orders:cart')
                
                OrderItem.objects.create(
                    order=order,
                    part=cart_item.part,
                    quantity=cart_item.quantity,
                    price=cart_item.part.price
                )
                
                cart_item.part.stock -= cart_item.quantity
                cart_item.part.save()
            
            order.calculate_total()
            cart.items.all().delete()
            
            messages.success(request, f'Order {order.id} placed successfully!')
            return redirect('orders:order_detail', order_id=order.id)
    
    return render(request, 'orders/checkout.html', {'cart': cart})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})
