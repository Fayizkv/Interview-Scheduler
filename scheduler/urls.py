from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('candidate/', views.candidate_view, name='candidate'),
    path('interviewer/', views.interviewer_view, name='interviewer'),
    path('hr_dashboard/', views.hr_dashboard, name='hr_dashboard'),
]
