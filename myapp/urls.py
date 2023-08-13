from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('', views.home),
    path('new/',views.home1),
    path('new/new',views.home1),
    path('valve/',views.home2),
    path('valve/valve',views.home2),
    path('shadow/',views.home3),
    path('shadow/shadow',views.home3),
    path('poi/',views.home4),
    path('poi/poi',views.home4),
]
