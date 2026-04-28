from rest_framework import filters, generics, status
from rest_framework.response import Response

from .models import Room
from .serializers import RoomSerializer
from .services import RoomService


class BaseRoomApiView:
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    service_class = RoomService


class RoomListCreateApiView(BaseRoomApiView, generics.ListCreateAPIView):
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created_at", "price"]
    ordering = ["price"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = self.service_class()
        new_room = service.create_room(serializer.validated_data)
        return Response({"room_id": new_room.id}, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        service = self.service_class()
        return service.read_rooms_list()


class RoomDestroyApiView(BaseRoomApiView, generics.DestroyAPIView):
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        service = self.service_class()
        service.delete_room(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
