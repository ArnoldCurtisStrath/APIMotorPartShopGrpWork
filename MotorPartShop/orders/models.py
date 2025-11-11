from django.db import models
from django.contrib.auth.models import User
from parts.models import Part

class Order(models.Model):
	STATUS_CHOICES = [
		('pending', 'Pending'),
		('processing', 'Processing'),
		('shipped', 'Shipped'),
		('delivered', 'Delivered'),
		('cancelled', 'Cancelled'),
	]
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
	total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f"Order {self.id} - {self.user.username}"

	def calculate_total(self):
		total = sum(item.subtotal for item in self.items.all())
		self.total_price = total
		self.save()
		return total

class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
	part = models.ForeignKey(Part, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)
	price = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return f"{self.quantity}x {self.part.name}"

	@property
	def subtotal(self):
		return self.quantity * self.price

class Cart(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Cart - {self.user.username}"

	@property
	def total_price(self):
		return sum(item.subtotal for item in self.items.all())

	@property
	def item_count(self):
		return sum(item.quantity for item in self.items.all())

class CartItem(models.Model):
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
	part = models.ForeignKey(Part, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)

	class Meta:
		unique_together = ('cart', 'part')

	def __str__(self):
		return f"{self.quantity}x {self.part.name}"

	@property
	def subtotal(self):
		return self.quantity * self.part.price

# Create your models here.
