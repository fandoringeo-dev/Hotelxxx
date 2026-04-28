from django.db.models.query import QuerySet
from loguru import logger

from .models import Booking


class BookingService:
    def create_booking(self, validated_data: dict) -> Booking:
        new_booking = Booking.objects.create(**validated_data)
        logger.info(f"Booking created: id={new_booking.id}, room_id={new_booking.room_id}")
        return new_booking

    def delete_booking(self, instance: Booking) -> None:
        instance.delete()
        logger.info(f"Booking deleted: id={instance.id}")

    def read_list_bookings(self, room_id: str | None) -> QuerySet:
        if not room_id:
            return Booking.objects.none()

        queryset = Booking.objects.filter(room_id=room_id)
        return queryset
