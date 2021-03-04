from drf_yasg.utils import swagger_auto_schema
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


api_info = openapi.Info(
  title="Snippets API",
  default_version='v1',
  description="Genesis",
  terms_of_service="",
  contact=openapi.Contact(email=""),
  license=openapi.License(name=""),
)

schema_view = get_schema_view(
   api_info,
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# response for login
login_response_decorator = swagger_auto_schema(
    responses={200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'token': openapi.Schema(type=openapi.TYPE_STRING),
            'user': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'username': openapi.Schema(type=openapi.TYPE_STRING),
                }
            ),
        }
    )}
)

# response for update is_read event notofication
event_post_response_decorator = swagger_auto_schema(
    responses={204: ''}
)

# response for update is_read event notofication
event_detect_post_decorator = swagger_auto_schema(
    responses={204: ''},
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'html': openapi.Schema(type=openapi.TYPE_STRING),
        }
    )
)
