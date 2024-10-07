from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from email_login.models import User
from .models import UserNickname
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden

from mass.models import Event

def index(request):
    return render(request, 'website/index.html')

@login_required
def user_profile(request, user_id):
    user = User.objects.get(id=user_id)
    events = Event.objects.filter(creator=user)
    
    try:
        nickname = UserNickname.objects.get(user=user).nickname
    except UserNickname.DoesNotExist:
        nickname = UserNickname.random_nickname_generator()
        UserNickname.objects.create(user=user, nickname=nickname)
        user_nickname = UserNickname.objects.get(user=user)
        user_nickname.nickname = nickname
        user_nickname.save()


    context = {
        'user': user,
        'nickname': nickname,
        'events': events
    }
    return render(request, 'website/user_profile.html', context)

@login_required
def change_nickname(request):
    print(request.user)
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        if nickname:
            user = request.user
            user_nickname, created = UserNickname.objects.get_or_create(user=user)
            user_nickname.nickname = nickname
            user_nickname.save()
            return redirect('website:user_profile', user_id=user.id)
    return redirect('website:user_profile', user_id=request.user.id)