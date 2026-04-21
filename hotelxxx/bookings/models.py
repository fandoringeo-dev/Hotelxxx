from django.db import models

class Booking(models.Model):
    room = models.ForeignKey('rooms.Room', on_delete=models.CASCADE, related_name='bookings')
    date_start = models.DateField()
    date_end = models.DateField()

    def __str__(self):
        return f'Бронь "{self.room.description}" c {self.date_start} до {self.date_end}'