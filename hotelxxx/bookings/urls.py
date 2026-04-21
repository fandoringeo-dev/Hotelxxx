from django.urls import path
from bookings import views


urlpatterns = [
    path('<int:booking_id>/', views.index),
]