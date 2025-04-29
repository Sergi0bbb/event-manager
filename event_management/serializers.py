from rest_framework import serializers

from user.serializers import UserSerializer
from event_management.models import Event, EventRegistration


class EventRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = EventRegistration
        fields = ["id", "event", "user", "status", "registration_date"]
        read_only_fields = ["registration_date"]


class EventSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ["id", "title", "description", "date", "organizer"]


class EventDetailSerializer(EventSerializer):
    registrations = EventRegistrationSerializer(many=True, read_only=True)

    class Meta(EventSerializer.Meta):
        fields = EventSerializer.Meta.fields + ["registrations"]


class UserEventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = ["id", "event", "status"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)