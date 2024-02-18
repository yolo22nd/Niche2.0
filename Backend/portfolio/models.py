from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.FloatField(default=0.0)
    asset_allocation = models.TextField(default='')
    risk_level = models.CharField(max_length=10, choices=[
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ])    

    def __str__(self):
        return str(self.value)

class Asset(models.Model):
    name = models.CharField(max_length=200)
    asset_type = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField()
    stop_loss_level = models.FloatField(default=None, null=True, blank=True)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)

class Stock(models.Model):
    name = models.CharField(max_length=200)
    symbol = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    risk = models.DecimalField(max_digits=10, decimal_places=2)
    graph = models.DecimalField(max_digits=10, decimal_places=2)

class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=200)
    threshold_price = models.DecimalField(max_digits=10, decimal_places=2)