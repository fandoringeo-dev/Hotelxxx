from django.contrib import admin
from django.urls import path, include

from hotel import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hotel/', views.index)
]