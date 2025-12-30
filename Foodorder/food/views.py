from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import FoodItem, Category, Restaurant, Order

from decimal import Decimal

User = get_user_model()

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not all([first_name, last_name, username, email, phone, password1, password2]):
            messages.error(request, "All fields are required.")
            return redirect('register')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register')

        User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            phone=phone,
            password=make_password(password1)
        )

        messages.success(request, "Account created successfully. Please login.")
        return redirect('login')

    return render(request, 'register.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # 🔥 ROLE BASED REDIRECT
            if user.is_staff or user.is_superuser:
                return redirect('admin_dashboard')
            else:
                return redirect('user_home')

        messages.error(request, "Invalid username or password.")
        return redirect('login')

    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('index')


@login_required(login_url='login')
def user_home(request):
    foods = FoodItem.objects.all()
    return render(request, 'user_home.html', {'foods': foods})


def is_admin(user):
    return user.is_staff or user.is_superuser

User = get_user_model()

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html', {
        'food_count': FoodItem.objects.count(),
        'category_count': Category.objects.count(),
        'restaurant_count': Restaurant.objects.count(),
        'user_count': User.objects.count(),
    })


@user_passes_test(is_admin, login_url='login')
def add_food(request):
    categories = Category.objects.all()
    restaurants = Restaurant.objects.all()

    if request.method == "POST":
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        restaurant_id = request.POST.get('restaurant')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')

        FoodItem.objects.create(
            name=name,
            category_id=category_id,
            restaurant_id=restaurant_id,
            description=description,
            price=price,
            image=image
        )

        return redirect('admin_dashboard')

    return render(request, 'admin_addfood.html', {
        'categories': categories,
        'restaurants': restaurants
    })


@user_passes_test(is_admin, login_url='login')
def view_foods(request):
    foods = FoodItem.objects.all().order_by('-created_at')
    return render(request, 'admin_viewfood.html', {'foods': foods})

@user_passes_test(is_admin, login_url='login')
def delete_food(request, food_id):
    food = get_object_or_404(FoodItem, id=food_id)
    food.delete()
    return redirect('view_foods')

@user_passes_test(is_admin, login_url='login')
def edit_food(request, food_id):
    food = get_object_or_404(FoodItem, id=food_id)
    categories = Category.objects.all()
    restaurants = Restaurant.objects.all()

    if request.method == "POST":
        food.name = request.POST.get('name')
        food.category_id = request.POST.get('category')
        food.restaurant_id = request.POST.get('restaurant')
        food.description = request.POST.get('description')
        food.price = request.POST.get('price')
        food.is_available = request.POST.get('is_available') == 'on'

        if request.FILES.get('image'):
            food.image = request.FILES.get('image')

        food.save()
        return redirect('view_foods')

    return render(request, 'edit_food.html', {
        'food': food,
        'categories': categories,
        'restaurants': restaurants
    })

@user_passes_test(is_admin, login_url='login')
def add_category(request):
    if request.method == "POST":
        name = request.POST.get('name').strip()

        if name:
            Category.objects.create(name=name)
            return redirect('view_categories')

    return render(request, 'add_category.html')


@user_passes_test(is_admin, login_url='login')
def view_categories(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'view_categories.html', {'categories': categories})


@user_passes_test(is_admin, login_url='login')
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == "POST":
        category.name = request.POST.get('name').strip()
        category.save()
        return redirect('view_categories')

    return render(request, 'edit_category.html', {'category': category})


@user_passes_test(is_admin, login_url='login')
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('view_categories')


@user_passes_test(is_admin, login_url='login')
def add_restaurant(request):
    if request.method == "POST":
        name = request.POST.get('name').strip()
        location = request.POST.get('location').strip()

        if name and location:
            Restaurant.objects.create(name=name, location=location)
            return redirect('view_restaurants')

    return render(request, 'add_restaurant.html')


@user_passes_test(is_admin, login_url='login')
def view_restaurants(request):
    restaurants = Restaurant.objects.all().order_by('name')
    return render(request, 'view_restaurants.html', {'restaurants': restaurants})


@user_passes_test(is_admin, login_url='login')
def edit_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == "POST":
        restaurant.name = request.POST.get('name').strip()
        restaurant.location = request.POST.get('location').strip()
        restaurant.save()
        return redirect('view_restaurants')

    return render(request, 'edit_restaurant.html', {'restaurant': restaurant})


@user_passes_test(is_admin, login_url='login')
def delete_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    restaurant.delete()
    return redirect('view_restaurants')


@login_required(login_url='login')
def order_now(request, food_id):
    food = get_object_or_404(FoodItem, id=food_id)

    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1))
        total_price = Decimal(quantity) * food.price

        Order.objects.create(
            user=request.user,
            food=food,
            quantity=quantity,
            total_price=total_price
        )

        messages.success(request, "Your order has been placed successfully!")
        return redirect('user_home')

    return render(request, 'order_now.html', {'food': food})


@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-ordered_at')
    return render(request, 'my_orders.html', {'orders': orders})

@user_passes_test(is_admin, login_url='login')
def admin_orders(request):
    orders = Order.objects.select_related(
        'user', 'food', 'food__restaurant'
    ).order_by('-ordered_at')

    return render(request, 'admin_orders.html', {
        'orders': orders
    })

@user_passes_test(is_admin, login_url='login')
def admin_users(request):
    users = User.objects.all().order_by('-date_joined')

    return render(request, 'admin_users.html', {
        'users': users
    })