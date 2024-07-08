from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout #for enabling the authentication process.
from django.contrib import messages # for feedback
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm, UpdateUserForm, PasswordForm


def update_password(request):
    if request.user.is_authenticated:
        user = request.user
        # Did they fill out the form
        if request.method == 'POST':
            form = PasswordForm(user, request.POST)
            # is the form vcalid?
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set successfully")
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = PasswordForm(user)
            return render(request, 'update_password.html', {'form': form})
    else:
        messages.success(request, "You must be logged in")
        return redirect('home')
    # return render(request, 'update_password.html', {'form': form})


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        form = UpdateUserForm(request.POST or None, instance=current_user)

        if form.is_valid():
            form.save()
            login(request, current_user)
            messages.success(request, "User has been updated!!")
            return redirect('home')
        return render(request, 'update_user.html', {'form': form})
    else:
        messages.success(request, "You must be logged in!")
        return redirect('home')

    # return render(request, 'update_user.html', {'form': form})


# Create your views here.
def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})

def home(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})


def about(request):
    return render(request, 'about.html', {})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('You have been logged in'))
            return redirect('home')
        else:
            messages.error(request, ('There was an error logging in, try again'))
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out, Hope to see you soon."))
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # log in user
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, ('You have been registered, you can now login and logout'))
            return redirect('home')
        else:
            messages.success(request, ('There was an error during account registration, try agin'))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})


def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {'categories': categories})


def category(request, name):
    # replacing - for ' '
    name = name.replace('-', ' ')
#     checking for the category from the url
    try:
    #     look up the category
        category = Category.objects.get(name=name)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category': category})
    except:
        messages.error(request, 'That category does not exist!!')
        return redirect('home')