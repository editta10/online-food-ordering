from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Restaurant, Category, FoodItem, Order


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ('username', 'email', 'first_name', 'last_name', 'phone', 'is_staff')
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'phone')

    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone',)}),
    )


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name', 'location')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'restaurant', 'price', 'is_available')
    list_filter = ('category', 'restaurant', 'is_available')
    search_fields = ('name', 'description')
    list_editable = ('is_available',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'food', 'quantity', 'total_price', 'status', 'ordered_at')
    