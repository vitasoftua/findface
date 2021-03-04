"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

from fcm_django.api.rest_framework import (
    FCMDeviceAuthorizedViewSet,
    FCMDeviceViewSet,
)
from rest_framework.permissions import AllowAny

from rest_framework.routers import DefaultRouter

from .swagger import schema_view

urlpatterns = [
    path('admin/', admin.site.urls),

    # drf_yasg
    path(
        'swagger.json',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),
    path(
        'swagger',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    path(
        'redoc',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),

    # apps
    path('', include('accounts.urls')),
    path('', include('faces.urls')),
]

# fcm_django
FCMDeviceViewSet.permission_classes = AllowAny,

fcm_devices_urlpatterns = [
    path(
        'devices',
        FCMDeviceAuthorizedViewSet.as_view({'post': 'create'}),
        name='create_fcm_device'
    ),
    path(
        'devices/delete/<str:registration_id>',
        FCMDeviceViewSet.as_view({'delete': 'destroy'}),
        name='delete_fcm_device'
    ),
]

urlpatterns += [path('api/v1/', include(fcm_devices_urlpatterns))]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
