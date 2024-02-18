from django.urls import path
from . import views

urlpatterns = [
    path('buyStock/', views.buyStock),
    ]