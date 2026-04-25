from rest_framework import serializers

from .models import Booking
from rooms.models import Room


class BookingCreateSerializer(serializers.ModelSerializer):
    room_id = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), source='room')

    def validate(self, attrs):
        if attrs['start_date'] >= attrs['end_date']:
            raise serializers.ValidationError('Start date must be earlier then end date')
        return attrs
    
    
    class Meta:
        model = Booking
        fields = ['room_id', 'start_date', 'end_date']



class BookingListSerializer(serializers.ModelSerializer):
    booking_id = serializers.IntegerField(source='id')

    class Meta:
        model = Booking
        fields = ['booking_id', 'start_date', 'end_date']