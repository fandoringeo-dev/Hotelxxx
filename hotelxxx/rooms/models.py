from django.db import models

class Room(models.Model):
    class TypeRoom(models.TextChoices):
        STANDART = 'S', ('Стандартный номер')
        BDSM = 'B', ('Команта с приколами')
        VIP = 'V', ('Для блатных')


    type = models.CharField(choices=TypeRoom.choices, default=TypeRoom.STANDART, max_length=5)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return  self.description