from rest_framework import mixins, viewsets
from rest_framework.decorators import api_view, schema
from rest_framework.reverse import reverse
from rest_framework.response import Response
from ticketapi.api.models import Event
from ticketapi.api.serializers import EventDetailSerializer, EventSimpleSerializer


class EventViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin):
    """
    Get the list of all events.
    """
    queryset = Event.objects.all()
    serializer_class = EventSimpleSerializer


class EventDetailsViewSet(viewsets.GenericViewSet,
                          mixins.RetrieveModelMixin):
    """
    Get a single event.
    """
    queryset = Event.objects.all()
    serializer_class = EventDetailSerializer


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
