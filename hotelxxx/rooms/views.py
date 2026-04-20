from django.shortcuts import render
from django.http import HttpResponse


def index(request, room_id):
    return HttpResponse(f'<h1>Страница приложения номеров</h1><h2>room:{room_id} </h2>')
