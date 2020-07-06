from django.contrib import admin
from django.urls import path, include
# from login import views as login
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('page/', include('homepage.urls')),
    # path('login/', login.Login.as_view()),
    path('auth/', include('system.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='/page/homepage/'), name='logout'),
]
urlpatterns +=staticfiles_urlpatterns()

if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)