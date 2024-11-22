from django.urls import path
from . import views

urlpatterns = [
    path('candidate/', views.candidate_schedule, name='candidate_schedule'),
    path('interviewer/', views.interviewer_schedule, name='interviewer_schedule'),
    path('hr_dashboard/', views.hr_dashboard, name='hr_dashboard'),
]
