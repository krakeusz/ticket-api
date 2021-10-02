from rest_framework import viewsets
from rest_framework.decorators import api_view, schema
from rest_framework.reverse import reverse
from rest_framework.response import Response
from ticketapi.api.models import Event
from ticketapi.api.serializers import EventSerializer


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Get the list of all events, or a single event.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer


@api_view(['GET'])
@schema(None)
def root(request, format=None):
    """
    This is an API that allows reservation and payment for tickets of events.

    For more, see the [documentation section](docs/).
    """
    return Response({
        'docs': reverse('swagger-ui', request=request, format=format),
        'api': reverse('api-root', request=request, format=format),
    })
