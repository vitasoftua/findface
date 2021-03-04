import logging

import requests

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import StreamingHttpResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators import gzip
from django.views.generic import TemplateView

from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from core.swagger import event_detect_post_decorator
from .tasks import update_event_is_read_background, event_detect_crop_img
from .serializers import (
    EventCreateSerializer,
    EventNotificationSerializer,
)
from .models import Event, EventNotification
from .utils import VideoCamera, gen

logger = logging.getLogger(__name__)


class CameraView(LoginRequiredMixin, TemplateView):
    """Camera view."""
    template_name = 'faces/camera_detail.html'

    def get_context_data(self, **kwargs):
        headers = {'Authorization': 'Token ' + settings.FFS_API_TOKEN}
        ctx = super().get_context_data()
        cam_id = kwargs.get('cam_id')
        if cam_id:
            ctx['camera'] = requests.get(
                settings.FFS_API_URL + '/v1/camera/' + cam_id,
                headers=headers
            ).json()
        else:
            cam_list = requests.get(
                settings.FFS_API_URL + '/v1/camera/',
                headers=headers
            ).json()
            ctx['camera'] = cam_list[0] if cam_list else ''

        if ctx['camera']:
            ctx['events'] = Event.objects.filter(
                camera=ctx['camera']['id']).order_by('-datetime')[:50]
        return ctx


@gzip.gzip_page
def stream_view(request, cam_id):
    """
    Live stream view.
    :param request:
    :return: Response or None
    """
    headers = {'Authorization': 'Token ' + settings.FFS_API_TOKEN}
    camera = requests.get(
        settings.FFS_API_URL + '/v1/camera/' + cam_id,
        headers=headers
    ).json()
    try:
        frames_gen = gen(VideoCamera(camera_url=camera['url'], fps=10, size=[250, 141]))
        frames_gen.__next__()
        return StreamingHttpResponse(
            frames_gen,
            content_type="multipart/x-mixed-replace;boundary=frame",
        )
    except Exception as e:
        logging.error(e, exc_info=True)
        return HttpResponse(
            content_type="multipart/x-mixed-replace;boundary=frame"
        )


class EventCreateView(CreateAPIView):
    """Create event."""
    serializer_class = EventCreateSerializer
    permission_classes = AllowAny,


class EventUserQSMixin:
    """Overrides get_queryset and list methods."""

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        self.get_queryset().update(is_new=False)
        return response


class EventNotificationViewSet(EventUserQSMixin, ReadOnlyModelViewSet):
    """Event list and event detail."""
    serializer_class = EventNotificationSerializer
    queryset = EventNotification.objects.order_by('-event__datetime')

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        notification = self.get_object()

        # Update is read notification status.
        notification.is_read = True
        notification.save(update_fields=['is_read'])

        # Update is read event status.
        if not notification.event.is_read:
            event = notification.event
            event.is_read = True
            event.save(update_fields=['is_read'])

            # Update event background web.
            update_event_is_read_background.apply_async((event.id,))

        return response


class NewEventNotificationView(EventUserQSMixin, ListAPIView):
    """New notifications list."""
    serializer_class = EventNotificationSerializer
    queryset = EventNotification.objects.filter(
        is_new=True
    ).order_by('-event__datetime')
    pagination_class = None


@method_decorator(name='post', decorator=event_detect_post_decorator)
class FaceDetectView(APIView):
    """Detected face."""
    permission_classes = AllowAny,

    def post(self, request, *args, **kwargs):
        data = request.data
        event_detect_crop_img.apply_async((
            data['html'], data['full_img'], data['rect_left'],
            data['rect_top'], data['rect_right'], data['rect_bottom'],
        ))
        return Response(status=204)
