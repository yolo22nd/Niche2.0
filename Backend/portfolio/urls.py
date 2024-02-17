from django.urls import path
from . import views

urlpatterns = [
    path('by-risk/', views.get_stocks_by_risk),
    # Add other URL patterns here
]