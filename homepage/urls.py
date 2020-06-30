from django.contrib import admin
from django.urls import path
from homepage import views
from django.views import View
urlpatterns = [
    # path('question/', views.Menu.as_view(), name='menu'),
    # path('question/<int:question_id>', views.QuestionDetail.as_view(), name='question_detail'),
    path('', views.HomePage.as_view(), name='homepage')
]
