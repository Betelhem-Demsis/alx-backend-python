from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsOwner,IsParticipantOfConversation
from .filters import MessageFilter
class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating Conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__username', 'participants__email']
    permission_classes = [IsAuthenticated]
    permission_classes = [IsParticipantOfConversation]

    @action(detail=False, methods=['post'])
    def create_conversation(self, request):
        """
        Custom action to create a new conversation with specified participants.
        """
        participant_ids = request.data.get('participants', [])
        if not participant_ids or len(participant_ids) < 2:
            return Response(
                {"error": "A conversation must have at least two participants."},
                status=400
            )
        participants = User.objects.filter(id__in=participant_ids)
        if participants.count() != len(participant_ids):
            return Response(
                {"error": "One or more participants do not exist."},
                status=400
            )
        
       
        if request.user not in participants:
            return Response(
                {"error": "You must be a participant in the conversation."},
                status=400
            )

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()
        return Response(ConversationSerializer(conversation).data, status=201)

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and sending Messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter, filters.DjangoFilterBackend]
    filterset_class = MessageFilter
    search_fields = ['sender__username', 'message_body']
    permission_classes = [IsAuthenticated, IsOwner] 

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """
        Custom action to send a message to an existing conversation.
        """
        conversation = self.get_object()  
        sender_id = request.data.get('sender_id')
        message_body = request.data.get('message_body')

        if not sender_id or not message_body:
            return Response(
                {"error": "Sender ID and message body are required."},
                status=400
            )

        sender = User.objects.filter(id=sender_id).first()
        if not sender:
            return Response({"error": "Sender does not exist."}, status=404)

       
        if sender not in conversation.participants.all():
            return Response(
                {"error": "Sender must be a participant in the conversation."},
                status=400
            )

        message = Message.objects.create(
            sender=sender,
            conversation=conversation,
            message_body=message_body
        )
        return Response(MessageSerializer(message).data, status=201)
