from datetime import date

from rest_framework import status
from rest_framework.test import APITestCase

from rooms.models import Room

from .models import Booking


class BookingsTests(APITestCase):
    def create_room(self, room_type="S", description="Room", price=3000):
        """Создает комнату в тестовой базе и возвращает объект."""
        return Room.objects.create(type=room_type, description=description, price=price)

    def create_booking(self, room, start_date, end_date):
        """Создает бронь в тестовой базе и возвращает объект."""
        return Booking.objects.create(room=room, start_date=start_date, end_date=end_date)

    def test_create_booking(self):
        """
        POST /bookings/ должен создать бронь и вернуть только booking_id.
        """
        room = self.create_room()
        data = {
            "room_id": room.id,
            "start_date": "2026-05-10",
            "end_date": "2026-05-12",
        }

        response = self.client.post("/api/v1/bookings/", data=data, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            msg="Booking was not created",
        )
        self.assertEqual(
            set(response.data.keys()),
            {"booking_id"},
            msg="Response must contain only booking_id",
        )
        self.assertEqual(
            Booking.objects.count(),
            1,
            msg="Booking was not saved in database",
        )

    def test_get_bookings_list_by_room_id(self):
        """
        GET /bookings/list?room_id=<id> должен вернуть только брони указанной комнаты.
        """
        first_room = self.create_room(description="First room")
        second_room = self.create_room(description="Second room")

        first_booking = self.create_booking(
            room=first_room,
            start_date=date(2026, 5, 10),
            end_date=date(2026, 5, 12),
        )
        self.create_booking(
            room=second_room,
            start_date=date(2026, 5, 11),
            end_date=date(2026, 5, 13),
        )

        response = self.client.get(
            f"/api/v1/bookings/list?room_id={first_room.id}",
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1, msg="Response contains extra bookings")
        self.assertEqual(response.data[0]["booking_id"], first_booking.id)
        self.assertEqual(
            set(response.data[0].keys()),
            {"booking_id", "start_date", "end_date"},
            msg="Booking response structure is incorrect",
        )

    def test_get_bookings_list_returns_empty_list_when_room_has_no_bookings(self):
        """
        GET /bookings/list?room_id=<id> должен вернуть пустой список, если у комнаты нет броней.
        """
        room = self.create_room()

        response = self.client.get(
            f"/api/v1/bookings/list?room_id={room.id}",
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [], msg="Response must be an empty list")

    def test_get_bookings_list_is_sorted_by_start_date_ascending_by_default(self):
        """
        GET /bookings/list?room_id=<id> должен по умолчанию сортировать брони по start_date по возрастанию.
        """
        room = self.create_room()
        earlier_booking = self.create_booking(
            room=room,
            start_date=date(2026, 5, 10),
            end_date=date(2026, 5, 12),
        )
        later_booking = self.create_booking(
            room=room,
            start_date=date(2026, 5, 15),
            end_date=date(2026, 5, 17),
        )

        response = self.client.get(
            f"/api/v1/bookings/list?room_id={room.id}",
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["booking_id"], earlier_booking.id)
        self.assertEqual(response.data[1]["booking_id"], later_booking.id)

    def test_get_bookings_list_can_be_sorted_by_start_date_descending(self):
        """
        GET /bookings/list?room_id=<id>&ordering=-start_date должен сортировать брони по start_date по убыванию.
        """
        room = self.create_room()
        earlier_booking = self.create_booking(
            room=room,
            start_date=date(2026, 5, 10),
            end_date=date(2026, 5, 12),
        )
        later_booking = self.create_booking(
            room=room,
            start_date=date(2026, 5, 15),
            end_date=date(2026, 5, 17),
        )

        response = self.client.get(
            f"/api/v1/bookings/list?room_id={room.id}&ordering=-start_date",
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["booking_id"], later_booking.id)
        self.assertEqual(response.data[1]["booking_id"], earlier_booking.id)

    def test_delete_booking(self):
        """
        DELETE /bookings/<id> должен удалить бронь из базы данных.
        """
        room = self.create_room()
        booking = self.create_booking(
            room=room,
            start_date=date(2026, 5, 10),
            end_date=date(2026, 5, 12),
        )

        response = self.client.delete(f"/api/v1/bookings/{booking.id}", format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Booking.objects.count(), 0, msg="Booking was not deleted")

    def test_create_booking_with_invalid_dates_returns_error(self):
        """
        POST /bookings/ не должен создавать бронь, если start_date не раньше end_date.
        """
        room = self.create_room()
        data = {
            "room_id": room.id,
            "start_date": "2026-05-12",
            "end_date": "2026-05-12",
        }

        response = self.client.post("/api/v1/bookings/", data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Booking.objects.count(), 0)

    def test_create_overlapping_booking_for_same_room_returns_error(self):
        """
        POST /bookings/ не должен создавать пересекающуюся бронь для той же комнаты.
        """
        room = self.create_room()
        self.create_booking(
            room=room,
            start_date=date(2026, 5, 10),
            end_date=date(2026, 5, 15),
        )

        data = {
            "room_id": room.id,
            "start_date": "2026-05-12",
            "end_date": "2026-05-16",
        }

        response = self.client.post("/api/v1/bookings/", data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Booking.objects.count(), 1)

    def test_create_booking_for_different_room_with_same_dates_is_allowed(self):
        """
        POST /bookings/ должен разрешать такую же дату брони для другой комнаты.
        """
        first_room = self.create_room(description="First room")
        second_room = self.create_room(description="Second room")

        self.create_booking(
            room=first_room,
            start_date=date(2026, 5, 10),
            end_date=date(2026, 5, 15),
        )

        data = {
            "room_id": second_room.id,
            "start_date": "2026-05-10",
            "end_date": "2026-05-15",
        }

        response = self.client.post("/api/v1/bookings/", data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 2)
