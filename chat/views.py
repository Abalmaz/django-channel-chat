import json

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.safestring import mark_safe

from chat.models import Room


def sign_up(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('registration:log_in'))
        else:
            print(form.errors)
    return render(request, 'registration/sign_up.html', {'form': form})


def user_list(request):
    return render(request, 'chat/user_list.html')


def index(request):
    rooms = Room.objects.order_by("title")
    return render(request, 'chat/index.html', {"rooms": rooms})


def room(request, room_name):
    room = Room.objects.get_or_new(room_name)
    messages = room.messages
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'messages': messages
    })
