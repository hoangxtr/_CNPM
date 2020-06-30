from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=25, unique=False)
    username = models.CharField(max_length=30, default='root', unique=True)
    password = models.CharField(max_length=30, unique=False)
    models.EmailField(max_length=254)

    def __str__(self):
        return self.name

class Admin(models.Model):
    name = models.CharField(max_length=25, unique=False)
    username = models.CharField(max_length=30, default='root', unique=True)
    password = models.CharField(max_length=30, unique=False)
    isManage = models.BooleanField(default=0)

    def __str__(self):
        return self.name

class Chef(models.Model):
    name = models.CharField(max_length=25, unique=False)
    username = models.CharField(max_length=30, default='root', unique=True)
    password = models.CharField(max_length=30, unique=False)

    def __str__(self):
        return self.name
    