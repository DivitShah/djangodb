from django.shortcuts import render,redirect, get_object_or_404
from django.db import transaction as db_transaction
from .models import User, Stock, Transaction
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib import messages
from django.db.models import Sum  # Import Sum
from django.contrib.auth.decorators import login_required
from . import models
# Create your views here.
def home(request):
    all_users = User.objects.all()
    return render(request,'home.html',{'users':all_users})

def join(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            form.save()
        else:
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            password = request.POST['password']
            age = request.POST['age']

            messages.error(request,('Invalid Information'))
            return render(request,'accounts/register.html',{'fname':fname,'lname':lname,'email':email,'password':password,'age':age})
        messages.success(request,('Your form has been submitted successfully!'))
        return redirect('home')
    else:
        return render(request,'accounts/register.html',{})
   

def custom_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            try:
                user = User.objects.get(email=email, password=password)  # Simple authentication, improve with hashing
                request.session['user_id'] = user.id
                return redirect('redirect_to_apple')
            except User.DoesNotExist:
                messages.error(request, 'Invalid email or password')
    else:
        form = UserLoginForm()
    return render(request, 'website/login.html', {'form': form})

def redirect_to_apple(request):
    return redirect('stock_detail', stock_name='Apple')

def get_logged_in_user(request):
    user_id = request.session.get('user_id')
    if user_id:
        return get_object_or_404(User, id=user_id)
    return None

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not get_logged_in_user(request):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
def stock_detail(request, stock_name):
    stock = get_object_or_404(Stock, name=stock_name)
    user = get_logged_in_user(request)
    return render(request, 'website/stock_detail.html', {'stock': stock, 'user': user})

@login_required
def buy_stock(request, stock_name):
    stock = get_object_or_404(Stock, name=stock_name)
    user = get_logged_in_user(request)

    if request.method == 'POST':
        quantity_to_buy = request.POST.get('quantity')
        if not quantity_to_buy or not quantity_to_buy.isdigit() or int(quantity_to_buy) <= 0:
            messages.error(request, 'Please enter a valid quantity.')
            return redirect('stock_detail', stock_name=stock.name)

        quantity_to_buy = int(quantity_to_buy)
        price = stock.price
        total_cost = quantity_to_buy * price

        if quantity_to_buy > stock.quantity:
            messages.error(request, 'Not enough stock available.')
            return redirect('stock_detail', stock_name=stock.name)

        if total_cost > user.capital:
            messages.error(request, 'Not enough capital available.')
            return redirect('stock_detail', stock_name=stock.name)

        try:
            with db_transaction.atomic():
                stock.quantity -= quantity_to_buy
                stock.save()

                user.capital -= total_cost
                user.save()

                Transaction.objects.create(
                    user=user,
                    stock=stock,
                    transaction_type='buy',
                    price=price,
                    quantity=quantity_to_buy
                )
                messages.success(request, 'Stock purchased successfully.')
        except Exception as e:
            messages.error(request, f'Error processing transaction: {e}')

        return redirect('stock_detail', stock_name=stock.name)
    else:
        return render(request, 'website/stock_detail.html', {'stock': stock})

@login_required
def sell_stock(request, stock_name):
    stock = get_object_or_404(Stock, name=stock_name)
    user = get_logged_in_user(request)

    if request.method == 'POST':
        quantity_to_sell = request.POST.get('quantity')
        if not quantity_to_sell or not quantity_to_sell.isdigit() or int(quantity_to_sell) <= 0:
            messages.error(request, 'Please enter a valid quantity.')
            return redirect('stock_detail', stock_name=stock.name)

        quantity_to_sell = int(quantity_to_sell)
        price = stock.price
        total_gain = quantity_to_sell * price

        user_holding = Transaction.objects.filter(user=user, stock=stock, transaction_type='buy').aggregate(total_bought=Sum('quantity'))['total_bought'] or 0
        user_sold = Transaction.objects.filter(user=user, stock=stock, transaction_type='sell').aggregate(total_sold=Sum('quantity'))['total_sold'] or 0
        user_available = user_holding - user_sold

        if quantity_to_sell > user_available:
            messages.error(request, 'Not enough stock owned to sell.')
            return redirect('stock_detail', stock_name=stock.name)

        try:
            with db_transaction.atomic():
                stock.quantity += quantity_to_sell
                stock.save()

                user.capital += total_gain
                user.save()

                Transaction.objects.create(
                    user=user,
                    stock=stock,
                    transaction_type='sell',
                    price=price,
                    quantity=quantity_to_sell
                )
                messages.success(request, 'Stock sold successfully.')
        except Exception as e:
            messages.error(request, f'Error processing transaction: {e}')

        return redirect('stock_detail', stock_name=stock.name)
    else:
        return render(request, 'website/stock_detail.html', {'stock': stock})
