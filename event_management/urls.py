from django.urls import path, include
from rest_framework.routers import DefaultRouter

from event_management.views import EventViewSet, EventRegistrationViewSet

router = DefaultRouter()
router.register(r"events", EventViewSet, basename="event")
router.register(r"event-registrations", EventRegistrationViewSet, basename="eventregistration")

urlpatterns = [
    path("", include(router.urls)),
]
