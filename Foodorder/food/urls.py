from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('home/', views.user_home, name='user_home'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/add-food/', views.add_food, name='add_food'),
    path('dashboard/view-foods/', views.view_foods, name='view_foods'),
    path('dashboard/delete-food/<int:food_id>/', views.delete_food, name='delete_food'),
    path('dashboard/edit-food/<int:food_id>/', views.edit_food, name='edit_food'),
    path('dashboard/add-category/', views.add_category, name='add_category'),
    path('dashboard/view-categories/', views.view_categories, name='view_categories'),
    path('dashboard/edit-category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('dashboard/delete-category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('dashboard/add-restaurant/', views.add_restaurant, name='add_restaurant'),
    path('dashboard/view-restaurants/', views.view_restaurants, name='view_restaurants'),
    path('dashboard/edit-restaurant/<int:restaurant_id>/', views.edit_restaurant, name='edit_restaurant'),
    path('dashboard/delete-restaurant/<int:restaurant_id>/', views.delete_restaurant, name='delete_restaurant'),
    path('order/<int:food_id>/', views.order_now, name='order_now'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('dashboard/admin/orders/', views.admin_orders, name='admin_orders'),
    path('dashboard/admin/users/', views.admin_users, name='admin_users'),






    
]