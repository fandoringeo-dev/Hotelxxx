from rest_framework import filters, generics, status
from rest_framework.response import Response

from .models import Booking
from .serializers import (
    BookingCreateSerializer,
    BookingListSerializer,
)
from .services import BookingService


class BaseBookingApiView:
    queryset = Booking.objects.all()
    service_class = BookingService


class BookingCreateApiView(BaseBookingApiView, generics.CreateAPIView):
    serializer_class = BookingCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = self.service_class()
        new_booking = service.create_booking(serializer.validated_data)
        return Response({"booking_id": new_booking.id}, status=status.HTTP_201_CREATED)


class BookingListApiView(BaseBookingApiView, generics.ListAPIView):
    serializer_class = BookingListSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["start_date"]
    ordering = ["start_date"]

    def get_queryset(self):
        room_id = self.request.query_params.get("room_id", None)
        service = self.service_class()
        return service.read_list_bookings(room_id)


class BookingDestroyApiView(BaseBookingApiView, generics.DestroyAPIView):
    serializer_class = BookingListSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        service = self.service_class()
        service.delete_booking(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
