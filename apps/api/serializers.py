from rest_framework import serializers
from apps.board.settings import SHOUTBOX_DISABLED_TAGS
from .models import Category, Subcategory, Thread, Post, \
    Conversation, Message, Report, Shout


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = '__all__'


class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'


class ShoutSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Shout
        fields = (
            'id', 'user', 'username', 'content', '_content_rendered', 'created',
            'modified')

    def create(self, validated_data):
        for key in SHOUTBOX_DISABLED_TAGS:
            key_tag = '[{}]'.format(key).lower()
            if key_tag[:len(key_tag) - 1] in validated_data.get('content').lower():
                raise serializers.ValidationError(
                    {'notAllowed': '{} is not allowed in the shoutbox'.format(key_tag)})
        return Shout.objects.create(**validated_data)
