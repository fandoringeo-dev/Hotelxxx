from rest_framework import serializers
from django.db.models import Q

from .models import Booking
from rooms.models import Room


class BookingCreateSerializer(serializers.ModelSerializer):
    room_id = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), source='room')

    def validate(self, attrs):
        if attrs['start_date'] >= attrs['end_date']:
            raise serializers.ValidationError('Start date must be earlier than end date')
        
        if Booking.objects.filter(Q(start_date__lt=attrs['end_date']) & Q(end_date__gt=attrs['start_date']) & Q(room_id=attrs['room'])):
            raise serializers.ValidationError('Room is already booked for the selected dates')
        return attrs
    
    
    class Meta:
        model = Booking
        fields = ['room_id', 'start_date', 'end_date']



class BookingListSerializer(serializers.ModelSerializer):
    booking_id = serializers.IntegerField(source='id')

    class Meta:
        model = Booking
        fields = ['booking_id', 'start_date', 'end_date']