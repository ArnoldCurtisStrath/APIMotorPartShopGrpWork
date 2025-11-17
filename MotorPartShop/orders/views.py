from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Order, OrderItem
from parts.models import Cart

# Create your views here.

@login_required
def checkout(request):
	cart = get_object_or_404(Cart, user=request.user)

	if not cart.items.exists():
		messages.warning(request, 'Your cart is empty.')
		return redirect('orders:cart')

	if request.method == 'POST':
		with transaction.atomic():
			# Create order
			order = Order.objects.create(user=request.user)

			# Create order items from cart items
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

				# Update stock
				cart_item.part.stock -= cart_item.quantity
				cart_item.part.save()

			# Calculate total
			order.calculate_total()

			# Clear cart
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
