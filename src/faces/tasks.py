import base64
from io import BytesIO

from PIL import Image
from celery import shared_task
from asgiref.sync import AsyncToSync

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone

from channels.layers import get_channel_layer
from fcm_django.models import FCMDevice

from accounts.models import User
from .models import Event, EventNotification
from .ws_serializers import EventNotificationSerializer, EventSerializer


def create_event_notification(event: Event) -> None:
    """
    Create event notifications and send them.
    :return:
    """
    users = User.objects.all()

    for user in users:
        event_notif = EventNotification.objects.create(
            event=event,
            user=user
        )

        # Send notifications via FCM.
        devices = FCMDevice.objects.filter(user=user)
        devices.send_message(
            title=event.detector,
            body='',
            data=EventNotificationSerializer(event_notif).data
        )


def update_channel_rooms(event: Event) -> None:
    """Update web notifications channel with event data."""
    channel_layer = get_channel_layer()

    AsyncToSync(channel_layer.group_send)(
        settings.ROOM_NAME_NOTIFICATIONS,
        {
            'type': 'chat_message',
            'message': EventSerializer(event).data
        },
    )


def update_face_event(event: Event) -> None:
    """Update faces channel with html contains event data."""
    channel_layer = get_channel_layer()

    # Detect
    html = '<img class="img-fluid rounded-top"  src="{}" alt=""/>' \
           '<div class="card-body p-0 m-0">' \
           '<p class="m-0 text-center">{}</p>' \
           '<p class="m-0 text-center">{}</p>' \
           '<p class="m-0 text-center">{}</p>' \
           '<p class="m-0 text-center">{}, {}</p>' \
           '</div>'.format(
                event.img.url,
                timezone.localtime(event.datetime).strftime("%d.%m.%y"),
                timezone.localtime(event.datetime).strftime("%H:%M:%S"),
                event.detector,
                event.age, event.gender,
           )

    AsyncToSync(channel_layer.group_send)(
        settings.ROOM_NAME_FACES,
        {
            'type': 'chat_message',
            'message': {'html': html, 'type': 'detect'}
        },
    )
    # Match
    html = '<img class="p-0 m-1 img-fluid rounded-top"  src="{}" alt=""/>' \
           '<div class="p-1 m-0"><p class="m-0 text-center">{}</p>' \
           '<p class="m-0 text-center">{}</p>' \
           '<p class="m-0 text-center">{}</p>' \
           '<p class="m-0 text-center">{}%</p>' \
           '<p class="m-0 text-center">{}</p></div>' \
           '<img class="p-0 m-1 img-fluid rounded-top" src="{}" alt=""/>'.format(
                event.img.url,
                timezone.localtime(event.datetime).strftime("%d.%m.%y"),
                timezone.localtime(event.datetime).strftime("%H:%M:%S"),
                event.detector,
                event.confidence,
                event.meta,
                event.face_link,
            )
    AsyncToSync(channel_layer.group_send)(
        settings.ROOM_NAME_FACES,
        {
            'type': 'chat_message',
            'message': {
                'html': html,
                'type': 'match',
                'id': f'match_{event.id}',
                'is_read': event.is_read,
            }
        },
    )


@shared_task
def update_face_event_detect(html: str) -> None:
    """Update faces channel with html contains event data."""
    channel_layer = get_channel_layer()
    AsyncToSync(channel_layer.group_send)(
        settings.ROOM_NAME_FACES,
        {
            'type': 'chat_message',
            'message': {'html': html, 'type': 'detect'}
        },
    )


@shared_task
def update_event_is_read_background(event_id: int) -> None:
    """Update background when event is_read."""
    channel_layer = get_channel_layer()
    AsyncToSync(channel_layer.group_send)(
        settings.ROOM_NAME_FACES,
        {
            'type': 'chat_message',
            'message': {'type': 'event_is_read', 'id': f'match_{event_id}'}
        },
    )


@shared_task
def event_crop_img(event_id: int) -> None:
    """Crop full_img."""
    event = Event.objects.get(id=event_id)
    path = settings.MEDIA_ROOT + '/'
    img = Image.open(path + event.full_img.name)
    thumb = img.crop((
        event.rect_left,
        event.rect_top,
        event.rect_right,
        event.rect_bottom,
    ))
    image_file = BytesIO()
    thumb.save(image_file, format='JPEG', quality=90)
    event.img.save(
        '_' + event.full_img.name.split('/')[-1],
        InMemoryUploadedFile(
            file=image_file,
            field_name=None,
            name='_' + event.full_img.name,
            content_type='image/jpeg',
            size=(),
            charset='utf8',
        ),
        save=False
    )
    event.save(update_fields=['img'])

    # Update web sockets.
    update_channel_rooms(event)
    update_face_event(event)

    # Create event notifications for users.
    create_event_notification(event)


@shared_task
def event_detect_crop_img(
        html: str, image: str, rect_left: int, rect_top: int,
        rect_right: int, rect_bottom: int) -> None:
    """Update faces channel with html contains event data."""

    img = Image.open(BytesIO(base64.b64decode(image)))
    thumb = img.crop((
        rect_left,
        rect_top,
        rect_right,
        rect_bottom,
    ))
    thumb_contents = BytesIO()
    thumb.save(thumb_contents, format='JPEG', quality=80)
    res_img = base64.b64encode(thumb_contents.getvalue()).decode()

    _html = '<img class="img-fluid rounded-top" ' \
            'src="data:image/jpeg;base64,{}" alt=""/>{}'.format(
                res_img,
                html
            )

    update_face_event_detect(_html)

