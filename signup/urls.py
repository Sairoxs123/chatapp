from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = "signup"),
    path('api/signup/', views.apiSignup, name="api-signup")
]
