from django.shortcuts import render,redirect
from .models import User
from .forms import UserRegistrationForm
from django.contrib import messages
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
            return render(request,'join.html',{'fname':fname,'lname':lname,'email':email,'password':password,'age':age})
        messages.success(request,('Your form has been submitted successfully!'))
        return redirect('home')
    else:
        return render(request,'join.html',{})