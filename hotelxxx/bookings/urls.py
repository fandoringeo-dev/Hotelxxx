from django.urls import path

from .views import BookingCreateApiView, BookingListApiView, DestroyApiView

urlpatterns = [
    path("", BookingCreateApiView.as_view(), name="booking-create"),
    path("list", BookingListApiView.as_view(), name="booking-list"),
    path("<int:pk>", DestroyApiView.as_view(), name="booking-delete"),
]
