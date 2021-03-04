import requests

from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def camera_list():
    """Lists all cameras."""
    headers = {'Authorization': 'Token ' + settings.FFS_API_TOKEN}
    cameras = requests.get(
        settings.FFS_API_URL + '/v1/camera/',
        headers=headers
    )
    return cameras.json()
