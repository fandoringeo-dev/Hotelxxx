from django.urls import path

from rooms import views

urlpatterns = [
    path('<int:room_id>/', views.index)
]