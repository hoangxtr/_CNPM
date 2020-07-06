from django.contrib import admin
from django.urls import path
from homepage import views
from django.views import View
app_name = 'homepage'
# app_name = 'homepage'
urlpatterns = [
    path('homepage/', views.HomePage.as_view(), name='homepage'),
    path('chefpage/', views.ChefPageOrder.as_view(), name='order'),
    path('chefpage/2/', views.ChefPageFoodDrink.as_view(), name='fooddrink'),
    path('adminpage/', views.AdminPage.as_view(), name='adminpage'),
    path('updatedItem/', views.updatedItem, name='updatedItem'),
    path('cart/', views.Cart.as_view(), name='cart'),
    path('wallet/', views.MyWallet.as_view(), name='mywallet'),
]