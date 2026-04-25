from django.db import models

class Booking(models.Model):
    room = models.ForeignKey('rooms.Room', on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Бронь "{self.room.description}" c {self.start_date} до {self.end_date}'