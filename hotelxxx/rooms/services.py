from django.db.models.query import QuerySet
from loguru import logger

from .models import Room


class RoomService:
    def create_room(self, validated_data: dict) -> Room:
        new_room = Room.objects.create(**validated_data)
        logger.info(f"Room created: id={new_room.id}")
        return new_room

    def delete_room(self, instance: Room) -> None:
        instance.delete()
        logger.info(f"Room deleted: id={instance.id}")

    def read_rooms_list(self) -> QuerySet:
        return Room.objects.all()
