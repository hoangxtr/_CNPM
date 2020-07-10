from django.contrib import admin
from django.urls import path
from homepage import views
from django.views import View

app_name = 'homepage'
urlpatterns = [
    path('homepage/', views.HomePage.as_view(), name='homepage'),
    path('adminpage/', views.AdminPage.as_view(), name='adminpage'),
    path('updatedItem/', views.updatedItem, name='updatedItem'),
    path('cart/', views.Cart.as_view(), name='cart'),
    path('profile/', views.Profile.as_view(), name="profile"),
    path('chefpage/', views.ChefPageOrder.as_view(), name='order'),
    path('chefpage/2/', views.ChefPageFoodDrink.as_view(), name='fooddrink'),
    path('wallet/', views.Wallet.as_view(), name='wallet'),
    path('wallet/login/', views.WalletLogin.as_view(), name='wallet_login'),
    #Phan them vo
    path('profile/', views.Profile.as_view(), name='profile'),
]