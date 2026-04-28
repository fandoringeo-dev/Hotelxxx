from django.urls import path

from .views import BookingCreateApiView, BookingDestroyApiView, BookingListApiView

urlpatterns = [
    path("", BookingCreateApiView.as_view(), name="booking-create"),
    path("list", BookingListApiView.as_view(), name="booking-list"),
    path("<int:pk>", BookingDestroyApiView.as_view(), name="booking-delete"),
]
