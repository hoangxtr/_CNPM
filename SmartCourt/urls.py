from django.contrib import admin
from django.urls import path, include
# from login import views as login
<<<<<<< HEAD
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static 
from django.contrib.auth import views as auth_views
from system.views import stream
=======
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static 
>>>>>>> 33099c2c05e6664c9b0ac30281128c00d2ff97b4
urlpatterns = [
    path('admin/', admin.site.urls),
    path('page/', include('homepage.urls')),
    # path('login/', login.Login.as_view()),
<<<<<<< HEAD
    # path('login/', include('system.urls')),
    path('auth/', include('system.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='/page/homepage/'), name='logout'),
    path('test/', stream, name='testing')
]

=======
    path('auth/', include('system.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='/page/homepage/'), name='logout'),
]
>>>>>>> 33099c2c05e6664c9b0ac30281128c00d2ff97b4
urlpatterns +=staticfiles_urlpatterns()

if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)