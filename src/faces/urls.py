from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views, consumers

urlpatterns = [
    path('', views.CameraView.as_view(), name='index'),
    path('camera/<slug:cam_id>', views.CameraView.as_view(), name='camera'),
    path('stream/<slug:cam_id>', views.stream_view, name='stream'),
    path('event/create', views.EventCreateView.as_view(), name='event_create'),
    path('event/detect', views.FaceDetectView.as_view(), name='face_detect'),

]

router = DefaultRouter(trailing_slash=False)
router.register('events', views.EventNotificationViewSet, basename='events')
api_urls = router.urls

api_urls += [
    path('new-events', views.NewEventNotificationView.as_view()),
]

urlpatterns += [path('api/v1/', include(api_urls))]


websocket_urlpatterns = [
    path('ws/notifications', consumers.NotificationConsumer),
    path('ws/faces', consumers.FaceConsumer),
]
