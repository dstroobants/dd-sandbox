from django.urls import path
from . import views

urlpatterns = [
    # Web views
    path('', views.home, name='home'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/create/', views.create_task, name='create_task'),
    
    # API endpoints
    path('health/', views.health_check, name='health_check'),
    path('api/', views.api_info, name='api_info'),
    path('tasks/api/', views.api_tasks, name='api_tasks'),
    path('categories/api/', views.api_categories, name='api_categories'),
] 
