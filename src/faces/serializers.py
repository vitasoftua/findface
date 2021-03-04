import base64
import uuid

from django.core.files.base import ContentFile
from rest_framework import serializers

from faces.tasks import event_crop_img
from .models import Event, EventNotification


class Base64ImageField(serializers.ImageField):
    """
    Encode img from base64.
    """

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            # base64 encoded image - decode
            format, imgstr = data.split(';base64,')  # format ~= data:image/X,
            ext = format.split('/')[-1]  # guess file extension
            id = uuid.uuid4()
            data = ContentFile(
                base64.b64decode(imgstr),
                name=id.urn[9:] + '.' + ext
            )
        return super(Base64ImageField, self).to_internal_value(data)


class EventCreateSerializer(serializers.ModelSerializer):
    """Serializer to create event."""

    full_img = Base64ImageField()

    class Meta:
        model = Event
        fields = (
            'id',
            'full_img',
            'face_link',
            'confidence',
            'meta',
            'camera',
            'detector',
            'age',
            'gender',
            'rect_left',
            'rect_top',
            'rect_right',
            'rect_bottom',
        )

    def create(self, validated_data):
        event = super().create(validated_data)

        # Update event image. After that update web sockets.
        event_crop_img.apply_async((event.id,))

        return event


class EventSerializer(serializers.ModelSerializer):
    """Event serializer to read."""
    face_link = serializers.SerializerMethodField()

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

    def get_face_link(self, event):
        return event.get_face_link(self.context.get('request'))


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
