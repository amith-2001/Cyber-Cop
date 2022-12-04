
from . import views
from django.urls import path
from app import views

urlpatterns = [
    path('api/', views.function1),
]
