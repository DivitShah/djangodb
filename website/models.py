from django.db import models
import datetime

# Create your models here.
class User(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)
    age = models.IntegerField()
    capital = models.DecimalField(default=10000, decimal_places=2, max_digits=10)

    def __str__(self):
        return self.fname+" "+self.lname
    
class Stock(models.Model):
    currencies = ['INR', 'USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'CHF', 'CNY', 'SEK', 'NZD', 'MXN', 'SGD', 'HKD', 'NOK', 'KRW', 'TRY', 'RUB', 'INR']
    ALL_CURRENCIES = sorted([(item, item) for item in currencies])

    
    name = models.CharField(max_length=100, default="")
    ticker = models.CharField(max_length=10, default="")
    currency = models.CharField(max_length=3, choices=ALL_CURRENCIES, default="INR")
    price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    if(currency == 'INR'):
        price = price*1
    elif(currency == 'USD'):
        price = price*85
    elif(currency == 'EUR'):
        price = price*90
    quantity = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.name

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('buy', 'Buy'),
        ('sell', 'Sell')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPE_CHOICES, default='buy')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    date = models.DateField(default=datetime.date.today)
    def __str__(self):
        return self.stock.name + " " + self.user.fname + " " + str(self.date) + " " + str(self.price) + " " + str(self.quantity)