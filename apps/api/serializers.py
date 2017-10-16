from django.contrib.auth import get_user_model
from rest_framework import serializers
from apps.board.settings import SHOUTBOX_DISABLED_TAGS
from .models import (
    Category, Subcategory, Thread, Post, Conversation, Message, Report, Shout)


class UserSerializer(serializers.ModelSerializer):
    rendered_username = serializers.ReadOnlyField()
    class Meta:
        model = get_user_model()
        exclude = ('password', 'groups', 'user_permissions',)
        read_only_fields = (
            'last_login', 'is_superuser', 'created', 'modified', 'email',
            'is_banned', 'username_modifier', 'rank', 'rendered_username',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubcategorySerializer(serializers.ModelSerializer):
    last_thread = serializers.ReadOnlyField(source='last_thread.id')
    last_thread_title = serializers.ReadOnlyField(source='last_thread.title')
    last_thread_created = serializers.ReadOnlyField(source='last_thread.created')
    last_thread_user = serializers.ReadOnlyField(source='last_thread.user.rendered_username')
    thread_count = serializers.ReadOnlyField()
    post_count = serializers.ReadOnlyField()
    class Meta:
        model = Subcategory
        fields = '__all__'


class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = '__all__'
        read_only_fields = ('pinned', 'closed', 'user',
                            'upvoted_by', 'downvoted_by',)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('user', 'upvoted_by', 'downvoted_by',)


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'
        read_only_fields = ('unread_by',)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ('user',)


class ShoutSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    rendered_username = serializers.ReadOnlyField(source='user.rendered_username')

    class Meta:
        model = Shout
        fields = (
            'id', 'user', 'username', 'rendered_username', 'content',
            '_content_rendered', 'created', 'modified')
        read_only_fields = ('user', )

    def create(self, validated_data):
        for key in SHOUTBOX_DISABLED_TAGS:
            key_tag = '[{}]'.format(key).lower()
            if key_tag[:len(key_tag) - 1] in validated_data.get('content').lower():
                raise serializers.ValidationError(
                    {'notAllowed': '{} is not allowed in the shoutbox'.format(key_tag)})
        return Shout.objects.create(**validated_data)
