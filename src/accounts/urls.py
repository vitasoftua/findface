from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.decorators import method_decorator

from rest_framework_jwt import views as jwt_views

from core.swagger import login_response_decorator
from . import views


urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),

    path(
        'user-data',
        views.UserTakeWebNotificationView.as_view(),
        name='user_data'
    ),
]

api_urls = [
    path(
        'token',
        method_decorator(
            name='post', decorator=login_response_decorator
        )(jwt_views.ObtainJSONWebToken).as_view(),
        name='token_obtain_pair'
    ),
    path(
        'token/refresh',
        method_decorator(
            name='post', decorator=login_response_decorator
        )(jwt_views.RefreshJSONWebToken).as_view(),
        name='token_refresh'
    ),
    path(
        'token/verify',
        method_decorator(
            name='post', decorator=login_response_decorator
        )(jwt_views.VerifyJSONWebToken).as_view(),
        name='token_verify'
    ),
]

urlpatterns += [path('api/v1/', include(api_urls))]
