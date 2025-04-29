from django.conf import settings
from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="organized_events"
    )

    def __str__(self):
        return self.title


class EventRegistration(models.Model):
    STATUS_CHOICES = [
        ("registered", 'Registered'),
        ("cancelled", 'Cancelled'),
    ]

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="registrations"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="event_registrations"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="registered"
    )
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.event.title} ({self.status})'
