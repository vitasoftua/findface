from .serializers import UserSerializer


def jwt_response_payload_handler(token, user=None, request=None) -> dict:
    """Control the response data returned after login or refresh."""
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }
