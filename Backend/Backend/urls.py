from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('base.api.urls')),
    path("portfolio/", include("portfolio.urls")),
    path("buy/", include("buy.urls")),
]