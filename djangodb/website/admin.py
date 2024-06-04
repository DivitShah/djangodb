from django.contrib import admin
from .models import User, Stock, Transaction
# Register your models here.
admin.site.register(User)
admin.site.register(Stock)
admin.site.register(Transaction)