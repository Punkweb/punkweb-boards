from django.contrib.auth import get_user_model
from rest_framework import serializers
from django_boards.conf.settings import SHOUTBOX_DISABLED_TAGS
from django_boards.models import (
    Category, Subcategory, Thread, Post, Conversation, Message, Report, Shout)


class UserSerializer(serializers.ModelSerializer):
    rendered_username = serializers.ReadOnlyField()
    rendered_rank = serializers.ReadOnlyField()
    post_count = serializers.ReadOnlyField()
    can_shout = serializers.ReadOnlyField()
    class Meta:
        model = get_user_model()
        exclude = ('password', 'groups', 'user_permissions',)
        read_only_fields = (
            'last_login', 'date_joined', 'is_staff', 'is_superuser', 'email',
            'username',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('auth_req',)


class SubcategorySerializer(serializers.ModelSerializer):
    last_thread = serializers.ReadOnlyField(source='last_thread.id')
    last_thread_title = serializers.ReadOnlyField(source='last_thread.title')
    last_thread_created = serializers.ReadOnlyField(source='last_thread.created')
    last_thread_user = serializers.ReadOnlyField(source='last_thread.user.profile.rendered_username')
    parent_name = serializers.ReadOnlyField(source='parent.name')
    thread_count = serializers.ReadOnlyField()
    post_count = serializers.ReadOnlyField()
    can_post = serializers.SerializerMethodField()

    def get_can_post(self, obj):
        return obj.can_post(self.context.get('request').user)

    class Meta:
        model = Subcategory
        exclude = ('auth_req',)


class ThreadSerializer(serializers.ModelSerializer):
    last_post = serializers.ReadOnlyField(source='last_post.id')
    last_post_created = serializers.ReadOnlyField(source='last_post.created')
    last_post_username = serializers.ReadOnlyField(source='last_post.user.username')
    last_post_rendered_username = serializers.ReadOnlyField(source='last_post.user.profile.rendered_username')
    user_username = serializers.ReadOnlyField(source='user.username')
    user_rendered_username = serializers.ReadOnlyField(source='user.profile.rendered_username')
    user_image = serializers.ReadOnlyField(source='user.profile.avatar')
    user_post_count = serializers.ReadOnlyField(source='user.profile.post_count')
    user_join_date = serializers.ReadOnlyField(source='user.created')
    flagged = serializers.ReadOnlyField(source='reported')
    posts_count = serializers.ReadOnlyField()
    can_edit = serializers.SerializerMethodField()

    def get_can_edit(self, obj):
        return obj.can_edit(self.context.get('request').user)

    class Meta:
        model = Thread
        fields = '__all__'
        read_only_fields = ('pinned', 'closed', 'user',
                            'upvoted_by', 'downvoted_by',)


class PostSerializer(serializers.ModelSerializer):
    flagged = serializers.ReadOnlyField(source='reported')
    can_edit = serializers.SerializerMethodField()

    def get_can_edit(self, obj):
        return obj.can_edit(self.context.get('request').user)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('user', 'upvoted_by', 'downvoted_by',)


class ConversationSerializer(serializers.ModelSerializer):
    last_message = serializers.ReadOnlyField(source='last_message.id')
    last_message_title = serializers.ReadOnlyField(source='last_message.title')
    last_message_created = serializers.ReadOnlyField(source='last_message.created')
    last_message_user = serializers.ReadOnlyField(source='last_message.user.profile.rendered_username')
    message_count = serializers.ReadOnlyField()
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
    rendered_username = serializers.ReadOnlyField(source='user.profile.rendered_username')

    class Meta:
        model = Shout
        fields = (
            'id', 'user', 'username', 'rendered_username', 'content',
            '_content_rendered', 'created', 'modified', )
        read_only_fields = ('user', )

    def create(self, validated_data):
        for key in SHOUTBOX_DISABLED_TAGS:
            key_tag = '[{}]'.format(key).lower()
            if key_tag[:len(key_tag) - 1] in validated_data.get('content').lower():
                raise serializers.ValidationError(
                    {'notAllowed': '{} is not allowed in the shoutbox'.format(key_tag)})
        return Shout.objects.create(**validated_data)
