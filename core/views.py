from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Product, Category, Profile
from .forms import SignUpForm, UserUpdateForm, PasswordChangeForm, InfoUpdateForm


def index(request):
    products = Product.objects.all()
    return render(request, 'core/index.html', {'products':products})


def about(request):
    return render(request, 'core/about.html', {})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user=user)
            messages.success(request, ("You have been logged in!"))
            return redirect('index')
        else:
            messages.error(request, ("There was an error. Kindly try again!"))
            return redirect('login')
    else:
        return render(request, 'core/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out!"))
    return redirect('index')


def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user=user)
                messages.success(request, ("You have registered successfully! Please fill your billing info below!"))
                return redirect('update_info')
            else:
                messages.error(request, ("There was an error. Kindly try logging in again"))
                return redirect('login')
        else:
            messages.error(request, ("Whoops! There was an error registering, please try again!"))
            return redirect('register')
    else:
        return render(request, 'core/register.html', {'form':form})
    

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UserUpdateForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            login(request, user=current_user)
            messages.success(request, ("Profile has been updated..."))
            return redirect('index')
        else:
            return render(request, 'core/update_user.html', {'user_form':user_form})        
    else:
        messages.success(request, ("Woah! Stop right there! Login First!"))
        return redirect('index')


def update_info(request):
    if request.user.is_authenticated:
        user_profile = Profile.objects.get(user=request.user)
        infoform = InfoUpdateForm(request.POST or None, instance=user_profile)
        if infoform.is_valid():
            infoform.save()
            messages.success(request, ("Profile Info updated..."))
            return redirect('update_info')
        
        return render(request, 'core/update_info.html', {'infoform':infoform})
    else:
        messages.success(request, ("Woah! Stop right there! Login First!"))
        return redirect('login')


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            password_form = PasswordChangeForm(current_user, request.POST)
            if password_form.is_valid():
                password_form.save()
                login(request, user=current_user)
                messages.success(request, ("Your password has been updated... Yayy!"))
                return redirect('update_user')
            else:
                for error in list(password_form.errors.values()):
                    messages.success(request, error)
                    return redirect('update_password')
        else:
            password_form = PasswordChangeForm(current_user)
            return render(request, 'core/update_password.html', {'password_form':password_form})
    else:
        messages.success(request, ("Woah! Stop right there! Login First!"))
        return redirect('index')  


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'core/product.html', {'product':product})


def search(request):
    # Determine if the form is filled.
    if request.method == 'POST':
        searched = request.POST['searched']
        # Query the Products DB Model
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        # print(searched[1].description)
        
        # check if product exists or not
        if not searched:
            messages.success(request, 'that product does not exist...')
            return render(request, 'core/search.html', {})
        else:
            return render(request, 'core/search.html', {'searched':searched})
    else:
        return render(request, 'core/search.html', {})


def category(request, cat):
    # Replace Hyphens with spaces
    cat = cat.replace('-', ' ')
    try:
        category = Category.objects.get(name=cat)
        products = Product.objects.filter(category=category)
        context = {"category":category,
                   "products":products}
        return render(request, 'core/category.html', context=context)
    except:
        messages.error(request, ("No such category exists. Please select a different one!"))
        return redirect('index')


def category_directory(request):
    categories = Category.objects.all()
    return render(request, 'core/category_directory.html', {'categories':categories})