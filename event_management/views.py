from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from event_management.models import Event, EventRegistration
from event_management.permissions import IsRegistrationUserOrReadOnly
from event_management.serializers import (
    EventSerializer,
    EventDetailSerializer,
    EventRegistrationSerializer,
    UserEventRegistrationSerializer
)


class EventViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Event.objects.select_related("organizer").all()

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ["organizer"]
    search_fields = ["title", "description"]
    ordering_fields = ["date", "created_at", "title"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return EventDetailSerializer
        return EventSerializer

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def register(self, request):
        event = self.get_object()
        serializer = UserEventRegistrationSerializer(
            data={"event": event.id, "status": "registered"},
            context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"])
    def registrations(self, request):
        event = self.get_object()
        if event.organizer != request.user:
            return Response(
                {"detail": "You do not have permission to view registrations for this event."},
                status=status.HTTP_403_FORBIDDEN
            )
        registrations = event.registrations.select_related("user").all()
        serializer = EventRegistrationSerializer(registrations, many=True)
        return Response(serializer.data)


class EventRegistrationViewSet(viewsets.ModelViewSet):
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated, IsRegistrationUserOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["event", "status"]

    def get_queryset(self):
        user = self.request.user
        base_qs = EventRegistration.objects.select_related("event", "user")
        return base_qs if user.is_staff else base_qs.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MyEventsView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Event.objects.select_related("organizer").filter(
            registrations__user=self.request.user,
            registrations__status="registered"
        )


class MyRegistrationsView(generics.ListAPIView):
    serializer_class = EventRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return EventRegistration.objects.select_related("event", "user").filter(user=self.request.user)