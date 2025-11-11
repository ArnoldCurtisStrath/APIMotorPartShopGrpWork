from django.contrib import admin
from .models import Order, OrderItem, Cart, CartItem

class OrderItemInline(admin.TabularInline):
	model = OrderItem
	extra = 0
	readonly_fields = ['subtotal']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'status', 'total_price', 'created_at']
	list_filter = ['status', 'created_at']
	search_fields = ['user__username', 'user__email']
	inlines = [OrderItemInline]

class CartItemInline(admin.TabularInline):
	model = CartItem
	extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
	list_display = ['user', 'item_count', 'total_price', 'created_at']
	inlines = [CartItemInline]
from django.contrib import admin

# Register your models here.
