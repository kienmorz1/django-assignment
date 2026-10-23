from rest_framework import serializers
from django.db import transaction
from typing import override
from .models import Event, Reservation
from django.db import IntegrityError
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title','venue','date','total_seats','available_seats']
        read_only_fields = ['status', 'created_at']

    @override
    def validate(self, data):
        total_seats = data.get(
            'total_seats',
            getattr(self.instance, 'total_seats', None),
        )
        available_seats = data.get(
            'available_seats',
            getattr(self.instance, 'available_seats', None),
        )

        if total_seats is None:
            raise serializers.ValidationError({
                'total_seats': 'This field cannot be null.'
            })

        if available_seats is None:
            raise serializers.ValidationError({
                'available_seats': 'This field cannot be null.'
            })

        if available_seats > total_seats:
            raise serializers.ValidationError({
                'available_seats': 'Available seats cannot exceed total seats.'
            })

        if self.instance is not None:
            errors = {}
            if total_seats < self.instance.total_seats:
                errors['total_seats'] = 'Total seats cannot be reduced.'
            if available_seats < self.instance.available_seats:
                errors['available_seats'] = 'Available seats cannot be reduced.'
            if errors:
                raise serializers.ValidationError(errors)

        return data

    @override
    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError as e:
            if 'total_and_available_seats_validation' in str(e):
                raise serializers.ValidationError({
                    'available_seats': 'Available Seats Cannot Exceed Total Seats'
                })
            raise serializers.ValidationError("A database constraint was violated.")


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model        = Reservation
        fields       = ['id', 'event', 'attendee_name', 'attendee_email',
        'seats_reserved', 'status', 'created_at','event']
        read_only_fields = ['status', 'created_at']

    def validate_seats_reserved(self, value):
        if value < 1:
            raise serializers.ValidationError('Must reserve at least 1 seat.')
        return value

    @override
    def validate(self, data):
        event = data.get('event')
        if event.status not in ('upcoming', 'ongoing'):
            raise serializers.ValidationError(
            f'Cannot reserve seats for a {event.status} event.'
            )
        if not event.available_seats:
            raise serializers.ValidationError(
            f'No Seats are available'
            )
        elif data.get('seats_reserved', 0) > event.available_seats:
            raise serializers.ValidationError(
            f'Only {event.available_seats} seat(s) available.'
            )
        return data

    @override
    def create(self, validated_data):
        try:
            with transaction.atomic():
                event = validated_data['event']
                event.available_seats -= validated_data['seats_reserved']
                event.save()
            return Reservation.objects.create(**validated_data)
        except Exception:
            raise Exception("Failed to book the event")
