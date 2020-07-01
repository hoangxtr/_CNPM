from django.urls import path
from .views import IndexClass
app_name = "main"
urlpatterns = [
    path('',IndexClass.as_view(), name="index"),
]