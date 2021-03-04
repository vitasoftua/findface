from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    is_take_web_notification = models.BooleanField(
        verbose_name=_('takes web notifications'),
        default=True
    )
