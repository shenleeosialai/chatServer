from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def chat_room(request, user_id):
    try:
        reciever = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponse("User not found.", status=404)
    
    sender = request.user
    latest_messages = reciever.chat_messages.select_related('user').order_by('-id')[:]
    latest_messages = reversed(latest_messages)
    
    return render(request,
                  'chat/room.html',
                  {'reciever': reciever,
                   'sender': sender,
                   'latest_messages': latest_messages})
    