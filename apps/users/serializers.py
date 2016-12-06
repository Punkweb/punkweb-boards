from django.contrib.auth import get_user_model
from rest_framework import serializers


class SettingsUserForSerializers:
    def __init__(self, *args, **kwargs):
        if not getattr(self.Meta, 'model', None):
            self.Meta.model = get_user_model()
        super().__init__(*args, **kwargs)


class EmailUserSerializer(SettingsUserForSerializers,
                          serializers.ModelSerializer):
    class Meta:
        read_only_fields = ('email', 'created', 'last_login', 'is_admin')
        exclude = ('password', 'groups', 'user_permissions',)
