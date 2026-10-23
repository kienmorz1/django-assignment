from django.test import SimpleTestCase

from .models import Event
from .serializers import EventSerializer


class EventSerializerValidationTests(SimpleTestCase):
    def setUp(self):
        self.event = Event(total_seats=100, available_seats=80)

    def test_rejects_reduced_total_seats(self):
        serializer = EventSerializer(
            self.event,
            data={'total_seats': 90},
            partial=True,
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn('total_seats', serializer.errors)

    def test_rejects_reduced_available_seats(self):
        serializer = EventSerializer(
            self.event,
            data={'available_seats': 70},
            partial=True,
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn('available_seats', serializer.errors)

    def test_allows_increasing_seat_counts(self):
        serializer = EventSerializer(
            self.event,
            data={'total_seats': 120, 'available_seats': 100},
            partial=True,
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
