from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'password')
        read_only_fields = ('id', )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=None,
            password=validated_data['password']
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = ("password", "groups", "user_permissions")
        read_only_fields = (
            "last_login",
            "date_joined",
            "is_staff",
            "is_superuser",
            "email",
            "username",
        )
