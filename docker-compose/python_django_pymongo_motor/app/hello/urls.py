from django.urls import path
from . import views

app_name = 'hello'
urlpatterns = [
    # Web views
    path('', views.index, name='index'),
    path('hello/', views.hello_html, name='hello_html'),
    path('sync/', views.mongodb_sync_demo, name='mongodb_sync'),
    path('async/', views.mongodb_async_demo, name='mongodb_async'),
    path('celery/', views.celery_demo, name='celery_demo'),
    
    # API endpoints
    path('api/users/', views.api_users, name='api_users'),
    path('api/posts/', views.api_posts, name='api_posts'),
    path('api/tasks/<str:task_id>/', views.api_task_status, name='api_task_status'),
    path('api/tasks/trigger/', views.api_trigger_task, name='api_trigger_task'),
]
