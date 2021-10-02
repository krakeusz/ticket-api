from datetime import timedelta
from django.db.models import IntegerField, Q
from django.db.models.functions import Cast
from django.utils import timezone
from rest_framework import serializers
from ticketapi.api.models import Event, Location, Seat, Ticket


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ['name', 'address']


class EventSerializer(serializers.HyperlinkedModelSerializer):
    location = LocationSerializer()
    remaining_seats = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['url', 'name', 'date', 'details',
                  'location', 'reservation_constraint', 'remaining_seats', 'pk']

    def get_remaining_seats(self, obj):
        reserved_tickets = Ticket.objects.filter(event__pk=obj.pk).filter(Q(reservation__is_paid=True) | Q(
            reservation__reservation_time__gte=timezone.now() - timedelta(minutes=15)))
        reserved_seats = [ticket.seat.number for ticket in reserved_tickets]
        remaining_seats = Seat.objects.filter(
            row__location__pk=obj.location.pk).exclude(id__in=reserved_seats).annotate(number_int=Cast('number', IntegerField())).order_by('number_int', 'number')
        if remaining_seats:
            return ", ".join(seat.number for seat in remaining_seats)
        return ""
