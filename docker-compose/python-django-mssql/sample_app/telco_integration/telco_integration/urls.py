from django.urls import path

from . import views

urlpatterns = [
    path("", views.hello, name="hello"),
    path("health/", views.health, name="health"),
    path("db/", views.db_check, name="db_check"),
    path("gateway/", views.gateway, name="gateway"),
    path("sleep/<int:seconds>/", views.sleep_view, name="sleep"),
]
