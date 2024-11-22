from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('availability/', views.availability_register, name='availability'),
    path('hr/', views.hr_dashboard, name='hr'),
]
