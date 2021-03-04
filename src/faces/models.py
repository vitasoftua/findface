from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext as _

from sorl.thumbnail import ImageField


class Event(models.Model):
    """Event model."""

    full_img = ImageField(_('full image'), upload_to='faces', null=True)
    img = ImageField(_('image'), upload_to='faces', null=True, blank=True)
    face_link = models.URLField(_('face link'))
    datetime = models.DateTimeField(_('datetime'), default=now)
    confidence = models.PositiveSmallIntegerField(_('confidence'))
    meta = models.TextField(_('meta'), blank=True)
    camera = models.UUIDField(_('camera id'))
    detector = models.CharField(_('camera detector'), max_length=50)
    age = models.SmallIntegerField(_('age'), blank=True, null=True)
    gender = models.CharField(_('gender'), blank=True, max_length=10)
    is_read = models.BooleanField(
        _('is read by at least one user'),
        default=False
    )
    rect_left = models.SmallIntegerField(default=0)
    rect_top = models.SmallIntegerField(default=0)
    rect_right = models.SmallIntegerField(default=0)
    rect_bottom = models.SmallIntegerField(default=0)

    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')

    def __str__(self):
        return str(self.camera)

    def get_face_link(self, request):
        """Override domain."""
        photo_url = self.face_link.replace(settings.FFS_UPLOAD_URL, '')
        return request.build_absolute_uri(photo_url)


class EventNotification(models.Model):
    """Event notification model."""

    event = models.ForeignKey(
        Event,
        verbose_name=_('event'),
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        'accounts.User',
        verbose_name=_('user'),
        on_delete=models.CASCADE
    )
    is_read = models.BooleanField(_('is read'), default=False)
    is_new = models.BooleanField(_('is new'), default=True)

    class Meta:
        verbose_name = _('event notification')
        verbose_name_plural = _('event notifications')

    def __str__(self):
        return str(self.event)
