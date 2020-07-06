from django.db import models
from homepage.models import Customer
# Create your models here.

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)

    def __str__(self):
	    return self.name

class Food(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    price = models.FloatField()
    description = models.TextField(max_length=300)
    image = models.TextField()
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	# transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)
	@property
	def get_total_amount(self):
		"""
			This function use for get total money of order
		"""
		return sum([item.get_total for item in self.orderitem_set.all()])
	@property
	def get_total_quantity(self):
		"""
			This function use for get total quantity of order
		"""
		return sum([item.quantity for item in self.orderitem_set.all()])

		


class OrderItem(models.Model):
	food = models.ForeignKey(Food, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)

	def __str__(self):
		return str(self.food.name)

	@property
	def get_total(self):
		"""
			get total money of order item
		"""
		total = self.food.price * self.quantity
		return total