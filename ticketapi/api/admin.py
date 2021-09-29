from django.contrib import admin
from ticketapi.api.models import *


class SeatInline(admin.StackedInline):
    model = Seat


class RowAdmin(admin.ModelAdmin):
    inlines = [
        SeatInline,
    ]


class RowInline(admin.StackedInline):
    model = Row


class LocationAdmin(admin.ModelAdmin):
    inlines = [
        RowInline,
    ]


admin.site.register(Event)
admin.site.register(Location, LocationAdmin)
admin.site.register(Reservation)
admin.site.register(Ticket)
admin.site.register(Row, RowAdmin)
