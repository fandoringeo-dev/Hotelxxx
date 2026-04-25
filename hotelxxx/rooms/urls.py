from django.urls import path

from .views import RoomListCreateApiView, RoomDestroyApiView

urlpatterns = [
    path('', RoomListCreateApiView.as_view(), name='room-list'),
    path('<int:pk>', RoomDestroyApiView.as_view(), name='room-destroy')
]