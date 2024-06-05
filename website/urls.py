from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('join',views.join,name="join"),
    path('login/', views.custom_login, name='login'),
    path('redirect/', views.redirect_to_apple, name='redirect_to_apple'),
    path('stock/<slug:stock_name>/buy/', views.buy_stock, name='buy_stock'),
    path('stock/<slug:stock_name>/sell/', views.sell_stock, name='sell_stock'),
    path('stock/<str:stock_name>/', views.stock_detail, name='stock_detail'),  # Add this line
]