from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('create/', views.create_survey, name='create_survey'),
    path('surveys/', views.survey_list, name='survey_list'),
    path('assigned_tasks/', views.assigned_tasks, name='assigned_tasks'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('change_status/<int:survey_id>/', views.change_status, name='change_status'),
]