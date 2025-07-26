from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import PrivateChatRoom,Message,Profile
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Count

@login_required
def home(request):
    return render(request, 'main/home.html')

@login_required
def profile_detail(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    return render(request, 'main/profile_detail.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_detail', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'main/profile_edit.html', {'form': form})


@login_required
def public_chat(request):
    messages = Message.objects.order_by('-timestamp')[:50]
    return render(request, 'main/public_chat.html', {'messages': messages})


@login_required
def send_message(request):
    if request.method == 'POST':
        content = request.POST.get('message')
        if content:
            Message.objects.create(user=request.user, content=content)
    return HttpResponseRedirect(reverse('public_chat'))

@login_required
def private_chat_view(request, username):
    other_user = get_object_or_404(User, username=username)

    if other_user == request.user:
        return redirect('profile_detail', username=username)

    rooms = PrivateChatRoom.objects.annotate(num_participants=Count('participants')).filter(
        participants=request.user,
        num_participants=2
    )

    room = None
    for r in rooms:
        if r.participants.filter(id=other_user.id).exists():
            room = r
            break

    # If no such room, create one
    if not room:
        room = PrivateChatRoom.objects.create()
        room.participants.set([request.user, other_user])
        room.save()

    messages = room.messages.all().order_by('timestamp')

    return render(request, 'main/private_chat.html', {
        'room': room,
        'other_user': other_user,
        'messages': messages,
    })

@login_required
def private_chat_list(request):
    user = request.user
    chats = PrivateChatRoom.objects.filter(participants=user)
    return render(request, 'main/private_chat_list.html', {'chats': chats})

