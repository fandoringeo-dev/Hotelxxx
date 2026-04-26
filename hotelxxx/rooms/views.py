from loguru import logger
from rest_framework import filters, generics, status
from rest_framework.response import Response

from .models import Room
from .serializers import RoomSerializer


class RoomListCreateApiView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created_at", "price"]
    ordering = ["price"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        logger.info(f"Room created: id={serializer.instance.id}")
        return Response({"room_id": serializer.instance.id}, status=status.HTTP_201_CREATED)


class RoomDestroyApiView(generics.DestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        logger.info(f"Room deleted: id={instance.id}")
        return Response(status=status.HTTP_204_NO_CONTENT)
