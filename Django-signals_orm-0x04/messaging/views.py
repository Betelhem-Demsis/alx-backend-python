from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory


@cache_page(60)
def conversation_view(request, conversation_id):
    conversation = Message.objects.prefetch_related('replies').filter(id=conversation_id)
    return render(request, 'conversation.html', {'conversation': conversation})


@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return redirect('home') 

def unread_messages_view(request):
    user = request.user
    unread_messages = Message.unread.unread_for_user(user).only('id', 'subject', 'sender', 'received_at')\
        .select_related('sender')  
    return render(request, 'messaging/unread_messages.html', {'messages': unread_messages})