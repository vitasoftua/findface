from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Login user serializer."""

    class Meta:
        model = User
        fields = ('id', 'username',)
