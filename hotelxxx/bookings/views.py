from loguru import logger
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
        logger.info(
            f"Booking created: id={serializer.instance.id}, room_id={serializer.instance.room_id}"
        )
        return Response({"booking_id": serializer.instance.id}, status=status.HTTP_201_CREATED)


class BookingListApiView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingListSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["start_date"]
    ordering = ["start_date"]

    def get_queryset(self):
        query = super().get_queryset()
        room_id = self.request.query_params.get("room_id", None)
        if room_id is None:
            return query.none()
        return query.filter(room_id=room_id)


class BookingDestroyApiView(generics.DestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingListSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        logger.info(f"Booking deleted: id={instance.id}")
        return Response(status=status.HTTP_204_NO_CONTENT)
