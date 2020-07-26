"""
from django.db import models
from django.contrib.auth.models import User
import os
# Create your models here.



class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    store = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=13, unique=False)
    name = models.CharField(max_length=30, unique=False)
    def __str__(self):
        return self.store


class vendor(models.Model):
    name = models.CharField(max_length=10, unique=True)
    owner = models.OneToOneField(Owner, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


def get_upload_path(instance, filename):
    return '{0}/{1}'.format(instance.store, filename)


class Food(models.Model):
    store = models.ForeignKey(vendor, on_delete=models.CASCADE)
    foodName = models.CharField(max_length=50)
    foodPrice = models.FloatField()
    foodDescription = models.TextField(max_length=500)
    foodState = models.BooleanField(default=True)
    foodImage = models.ImageField(upload_to=get_upload_path)
    foodQuantity = models.IntegerField()
    foodPrepare = models.IntegerField()

    def __str__(self):
        return self.foodName

class Chef(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='chef')
    store = models.ForeignKey(vendor, on_delete=models.CASCADE)
    name = models.CharField(max_length=25, unique=False)
    phone = models.CharField(max_length=13, unique=False)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Chefs"


class Order(models.Model):
    store = models.ForeignKey(vendor, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_total_amount(self):
        return sum([item.get_total for item in self.orderitem_set.all()])

    @property
    def get_total_quantity(self):
        return sum([item.quantity for item in order.orderitem_set.all()])


class OrderItem(models.Model):
	food = models.ForeignKey(Food, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)

	def __str__(self):
		return str(self.food.foodName)

	@property
	def get_total(self):
		total = self.food.foodPrice * self.quantity
		return total

"""

