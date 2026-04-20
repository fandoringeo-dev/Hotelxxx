from django.shortcuts import render
from django.http import HttpResponse


def index(request, booking_id):
    return HttpResponse('<h1>Страница приложения брони</h1>')
