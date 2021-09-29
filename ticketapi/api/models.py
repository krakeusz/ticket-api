from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Location(models.Model):
    address = models.CharField(max_length=400)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Row(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return f"Row of {self.location}"


class Seat(models.Model):
    number = models.CharField(max_length=10)
    row = models.ForeignKey(Row, on_delete=models.PROTECT)

    def __str__(self):
        return f"Seat {self.number} of {self.row.location}"


class Event(models.Model):

    class ReservationConstraint(models.TextChoices):
        NONE = 'NO', _('None')
        EVEN = 'EV', _('Even')
        ALL_TOGETHER = 'AT', _('All together')
        AVOID_ONE = 'AO', _('Avoid one')

    name = models.CharField(max_length=400)
    details = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    reservation_constraint = models.CharField(
        max_length=2, choices=ReservationConstraint.choices, default=ReservationConstraint.NONE)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    reservation_time = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    date = models.DateTimeField()

    def __str__(self):
        ticket_count = Ticket.objects.filter(pk=self.pk).count()
        return f"Reservation for {ticket_count} ticket(s) by {self.user.username} for {self.event.name}"


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    reservation = models.ForeignKey(
        Reservation, null=True, blank=True, on_delete=models.SET_NULL)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    seat = models.ForeignKey(Seat, on_delete=models.PROTECT)

    class Meta:
        unique_together = [['event', 'seat']]

    def __str__(self):
        return f"Ticket for seat {self.seat.number} on {self.event.name}"
