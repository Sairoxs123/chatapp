from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = "login"),
    path('api/login/', views.apiLogin, name="api-login")
]
