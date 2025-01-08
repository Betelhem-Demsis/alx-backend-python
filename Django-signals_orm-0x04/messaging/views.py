from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.contrib.auth.models import User
from .models import Message

@cache_page(60)
def conversation_view(request, conversation_id):
    """
    View for a single conversation, including all replies in a threaded format.
    """
    conversation = (
        Message.objects.filter(id=conversation_id)
        .select_related('sender', 'receiver')  # Optimize sender and receiver fields
        .prefetch_related('replies__sender')  # Prefetch replies and their senders
        .first()  # Fetch the single conversation
    )

    if not conversation:
        return render(request, '404.html', status=404)

    def get_threaded_replies(message):
        """
        Recursively fetch all replies for a message in a threaded format.
        """
        return {
            'message': message,
            'replies': [
                get_threaded_replies(reply)
                for reply in message.replies.all()
            ],
        }

    threaded_conversation = get_threaded_replies(conversation)

    return render(request, 'conversation.html', {'threaded_conversation': threaded_conversation})


@login_required
def delete_user(request):
    """
    Allow logged-in users to delete their account.
    """
    user = request.user
    user.delete()
    return redirect('home')


def unread_messages_view(request):
    """
    View to display all unread messages for the logged-in user.
    """
    user = request.user
    unread_messages = (
        Message.unread.unread_for_user(user)
        .only('id', 'subject', 'sender', 'received_at') 
        .select_related('sender')  
    )

    return render(request, 'messaging/unread_messages.html', {'messages': unread_messages})
