from rest_framework import filters, generics, status
from rest_framework.response import Response

from .models import Booking
from .serializers import (
    BookingCreateSerializer,
    BookingListSerializer,
)


class BookingCreateApiView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"booking_id": serializer.instance.id}, status=status.HTTP_201_CREATED)


class BookingListApiView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingListSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["start_date"]
    ordering = ["start_date"]

    def get_queryset(self):
        query = super().get_queryset()
        room_id = self.request.query_params["room_id"]
        return query.filter(room_id=room_id)


class DestroyApiView(generics.DestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingListSerializer
