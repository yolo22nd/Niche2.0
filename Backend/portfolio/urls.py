from django.urls import path
from . import views

urlpatterns = [
    path('by-risk/', views.get_stocks_by_risk),
    path('get_portfolio/', views.get_portfolio),
    path('check_stop_loss/', views.check_stop_loss),
]