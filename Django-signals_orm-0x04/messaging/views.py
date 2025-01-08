from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory


@cache_page(60)
def conversation_view(request, conversation_id):
    conversation = Message.objects.prefetch_related('replies').filter(id=conversation_id)
    return render(request, 'conversation.html', {'conversation': conversation})

def inbox_view(request):
    unread_messages = Message.objects.get_unread(request.user)
    return render(request, 'inbox.html', {'unread_messages': unread_messages})

@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return redirect('home') 
