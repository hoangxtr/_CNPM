from django.contrib import admin
from django.urls import path, include
# from login import views as login
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('page/', include('homepage.urls')),
    # path('login/', login.Login.as_view()),
    path('login/', include('system.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='/page/homepage/'), name='logout'),
]

