from rest_framework import generics
from .models import Room
from .serializers import RoomSerializer


class RoomApiView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer