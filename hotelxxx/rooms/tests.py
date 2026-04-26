from datetime import date, timedelta

from bookings.models import Booking
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Room


class RoomsTests(APITestCase):
    def create_room(self, room_type="S", description="Room", price=3000):
        """
        Создает комнату в тестовой базе и возвращает объект.
        """
        return Room.objects.create(type=room_type, description=description, price=price)

    def test_create_room(self):
        """
        POST /rooms/ должен создать комнату и вернуть только room_id.
        """
        data = {
            "type": "B",
            "description": "ebobo",
            "price": 69600,
        }

        response = self.client.post("/api/v1/rooms/", data=data, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            msg="Room was not created",
        )
        self.assertEqual(
            set(response.data.keys()),
            {"room_id"},
            msg="Response must contain only room_id",
        )
        self.assertEqual(Room.objects.count(), 1, msg="Room was not saved in database")

    def test_get_rooms_list(self):
        """
        GET /rooms/ должен вернуть сериализованный список комнат
        """

        self.create_room(room_type="S", description="Room 1", price=3000)
        self.create_room(room_type="V", description="Room 2", price=5000)

        response = self.client.get("/api/v1/rooms/", format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg="Rooms list was not returned",
        )
        self.assertEqual(len(response.data), 2, msg="Rooms count in response is incorrect")
        self.assertEqual(
            set(response.data[0].keys()),
            {"id", "type", "description", "price", "created_at", "updated_at"},
            msg="Room response structure is incorrect",
        )

    def test_get_rooms_list_is_sorted_by_price_ascending_by_default(self):
        """
        GET /rooms/ должен по умолчанию сортировать комнаты по цене по возрастанию.
        """
        cheap_room = self.create_room(description="Cheap room", price=1000)
        expensive_room = self.create_room(description="Expensive room", price=5000)

        response = self.client.get("/api/v1/rooms/", format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], cheap_room.id)
        self.assertEqual(response.data[1]["id"], expensive_room.id)

    def test_get_rooms_list_can_be_sorted_by_price_descending(self):
        """
        GET /rooms/?ordering=-price должен сортировать комнаты по цене по убыванию.
        """
        cheap_room = self.create_room(description="Cheap room", price=1000)
        expensive_room = self.create_room(description="Expensive room", price=5000)

        response = self.client.get("/api/v1/rooms/?ordering=-price", format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], expensive_room.id)
        self.assertEqual(response.data[1]["id"], cheap_room.id)

    def test_get_rooms_list_can_be_sorted_by_created_at_ascending(self):
        """
        GET /rooms/?ordering=created_at должен сортировать комнаты по дате создания по возрастанию.
        """
        older_room = self.create_room(description="Older room", price=2000)
        newer_room = self.create_room(description="Newer room", price=2000)

        now = timezone.now()
        Room.objects.filter(pk=older_room.pk).update(created_at=now - timedelta(days=1))
        Room.objects.filter(pk=newer_room.pk).update(created_at=now)

        response = self.client.get("/api/v1/rooms/?ordering=created_at", format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], older_room.id)
        self.assertEqual(response.data[1]["id"], newer_room.id)

    def test_get_rooms_list_can_be_sorted_by_created_at_descending(self):
        """
        GET /rooms/?ordering=-created_at должен сортировать комнаты по дате создания по убыванию.
        """
        older_room = self.create_room(description="Older room", price=2000)
        newer_room = self.create_room(description="Newer room", price=2000)

        now = timezone.now()
        Room.objects.filter(pk=older_room.pk).update(created_at=now - timedelta(days=1))
        Room.objects.filter(pk=newer_room.pk).update(created_at=now)

        response = self.client.get("/api/v1/rooms/?ordering=-created_at", format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], newer_room.id)
        self.assertEqual(response.data[1]["id"], older_room.id)

    def test_delete_room(self):
        """
        DELETE /rooms/<id> должен удалить комнату из базы данных.
        """
        room = self.create_room(description="Room to delete", price=2500)

        response = self.client.delete(f"/api/v1/rooms/{room.id}", format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Room.objects.count(), 0, msg="Room was not deleted from database")

    def test_delete_room_with_cascade_bookings(self):
        """
        DELETE /rooms/<id> должен удалить все брони на эту комнату
        """

        room = self.create_room(description="Room to delete", price=2500)
        Booking.objects.create(
            room_id=room.id, start_date=date(2026, 1, 1), end_date=date(2026, 1, 3)
        )
        Booking.objects.create(
            room_id=room.id, start_date=date(2026, 1, 4), end_date=date(2026, 1, 5)
        )

        response = self.client.delete(f"/api/v1/rooms/{room.id}", format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Booking.objects.count(), 0, msg="Booking was not deleted from database")
