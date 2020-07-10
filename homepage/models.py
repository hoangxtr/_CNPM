<<<<<<< HEAD
# from django.db import models
# from django.contrib.auth.models import User

# # Create your models here.
# class Customer(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
#     name = models.CharField(max_length=25, unique=False)
#     models.EmailField(max_length=254)

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name_plural = "Customers"

# class Admin(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin')
#     name = models.CharField(max_length=25, unique=False)
#     isManage = models.BooleanField(default=0)

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name_plural = "Admins"

# class Chef(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='chef')
#     name = models.CharField(max_length=25, unique=False)

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name_plural = "Chefs"
=======
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    name = models.CharField(max_length=25, unique=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Customers"

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin')
    name = models.CharField(max_length=25, unique=False)
    isManage = models.BooleanField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Admins"

class Chef(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='chef')
    name = models.CharField(max_length=25, unique=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Chefs"


class Notification(models.Model):
	is_closed = models.BooleanField(default=False)
	title = models.CharField(max_length=100)
	content = models.TextField(max_length=1000)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=False)

	def __str__(self):
		return self.title


>>>>>>> 33099c2c05e6664c9b0ac30281128c00d2ff97b4
