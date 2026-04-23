from rest_framework import generics, filters
from .models import Room
from .serializers import RoomSerializer


class RoomListCreateApiView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'price']
    ordering = ['price']


class RoomDestroyApiView(generics.DestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer