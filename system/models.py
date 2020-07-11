from django.db import models
# from homepage.models import Customer
from django.contrib.auth.models import User


# Create your models here.


class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    store = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=13, unique=False)
    name = models.CharField(max_length=30, unique=False)

    def __str__(self):
        return self.store


class Vendor(models.Model):
    name = models.CharField(max_length=10, unique=True)
    owner = models.OneToOneField(Owner, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    name = models.CharField(max_length=25, unique=False)
    email = models.EmailField(max_length=254, default='')
    phone = models.CharField(max_length=10, default='')
    avatar = models.ImageField(upload_to="uploads/", blank=True, null=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Customers"


class Chef(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='chef')
    store = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    name = models.CharField(max_length=25, unique=False)
    phone = models.CharField(max_length=13, unique=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Chefs"


def get_upload_path(instance, filename):
    return '{0}/{1}'.format(instance.vendor, filename)


class Food(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.FloatField()
    description = models.TextField(max_length=500)
    image = models.ImageField(upload_to=get_upload_path)
    quantity = models.IntegerField()
    prepare = models.IntegerField()

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    # store = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True)
    # 0 -> normal
    # 1 -> to_chef
    # 2 -> notify food already
    # 3 -> complete
    status = models.IntegerField(default=0)
    note = models.CharField(max_length=255, default='')
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_total_price(self):
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


class BankAccount(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=255, default='')
    image = models.ImageField(upload_to="uploads/")
    account_number = models.IntegerField(default=0)
    balance = models.FloatField(default=0)

    def __str__(self):
        return self.username


class MyWallet(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    my_account_number = models.IntegerField(default=0)
    my_balance = models.FloatField(default=0)


