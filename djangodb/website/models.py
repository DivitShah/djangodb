from django.db import models
import datetime

# Create your models here.
class User(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)
    age = models.IntegerField()

    def __str__(self):
        return self.fname+" "+self.lname
    
class Stock(models.Model):
    name = models.CharField(max_length=100, default="")
    ticker = models.CharField(max_length=10, default="")
    current_price = models.FloatField(default=0.0)
    previous_price = models.FloatField(default=0.0, null=True)
    quantity = models.IntegerField(default=0)
    def __str__(self):
        return self.name

class Transaction(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=False)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    is_buy = models.BooleanField(null=False, default=True)
    quantity = models.IntegerField(default=1)
    price = models.FloatField()
    date = models.DateField(default=datetime.date.today)
    def __str__(self):
        return self.stock.name + " " + self.buyer.fname + " " + str(self.date) + " " + str(self.price) + " " + str(self.quantity)