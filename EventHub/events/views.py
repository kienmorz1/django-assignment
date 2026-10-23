from rest_framework import status
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from .models import Event, Reservation
from .serializers import ReservationSerializer, EventSerializer
from rest_framework.viewsets import ModelViewSet
from .filters import EventFilter

# Create your views here.
class EventViewSet(ModelViewSet):

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filterset_class = EventFilter


class ReservationViewSet(ModelViewSet):

    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
    filterset_fields = ['event_id']
    http_method_names = ['get', 'post']


    @action(detail=True, methods=['POST'], url_path="cancel")
    def cancel(self, request, pk=None):
        reservation = self.get_object()
        if reservation.status == 'cancelled':
            return Response({'error': 'Already cancelled.'}, status=400)
        if reservation.event.available_seats + reservation.seats_reserved <= reservation.event.total_seats:
            reservation.event.available_seats += reservation.seats_reserved
        reservation.event.save()
        reservation.status = 'cancelled'
        reservation.save()
        return Response(self.get_serializer(reservation).data)
