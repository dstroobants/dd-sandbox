from django.urls import path
from . import views

app_name = 'hello'
urlpatterns = [
    path('', views.psycopg2_demo, name='psycopg2_demo'),
    path('html/', views.hello_html, name='hello_html'),
    path('api/users/', views.api_users, name='api_users'),
]
