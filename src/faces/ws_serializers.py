from rest_framework import serializers

from faces.models import Event, EventNotification


class EventSerializer(serializers.ModelSerializer):
    """Event serializer to read."""

    class Meta:
        model = Event
        fields = (
            'id',
            'img',
            'confidence',
            'meta',
            'camera',
            'detector',
            'datetime',
            'face_link',
        )


class EventNotificationSerializer(serializers.ModelSerializer):
    """Event Notification serializer to read."""

    event = EventSerializer()

    class Meta:
        model = EventNotification
        fields = (
            'id',
            'event',
            'is_read',
        )
