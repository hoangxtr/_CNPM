from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('manager/', views.man_homepage, name="manager"),
    path('dowload-report-owner/', views.makeOwnerReport, name="ownReport"),
    path('dowload-manager/', views.makeManReport, name="manReport"),
    path('owner/', views.owner_homepage.as_view(), name="owner"),
    path('manager/login/', views.manLogin, name="manLogin"),
    path('out/', views.Log_out, name='logout'),
    path('owner/login/', views.OwnerLogin, name='ownLogin'),
    path('delOwner/<pk>', views.delOwner, name='delOwner'),
    path('editOwner/<pk>', views.editOwner, name='editOwner'),
    path('delFood/<pk>', views.delFood, name='delFood'),
    path('editMenu/<pk>', views.editMenu, name='editMenu'),
    path('owner/addStaff', views.AddStaff, name='addStaff'),
    path('editStaff/<pk>', views.EditStaff, name='editStaff'),
    path('delStaff/<pk>', views.delStaff, name='delStaff'),
]


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
