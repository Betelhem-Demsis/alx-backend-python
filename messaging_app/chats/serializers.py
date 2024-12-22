from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    role = serializers.CharField()  

    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'role']


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.
    Includes validation for message_body.
    """
    sender_username = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender_id', 'sender_username', 'message_body', 'sent_at']
        read_only_fields = ['sent_at']

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        return value


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Conversation model.
    Includes nested messages and participants.
    """
    participants = UserSerializer(many=True)  
    messages = serializers.SerializerMethodField()  

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']

    def get_messages(self, obj):
        """
        Custom method to fetch all messages in the conversation.
        """
        messages = Message.objects.filter(conversation=obj).order_by('sent_at')
        return MessageSerializer(messages, many=True).data
