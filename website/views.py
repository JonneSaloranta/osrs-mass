from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from email_login.models import User
from .models import UserNickname
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden

def index(request):
    return render(request, 'website/index.html')

@login_required
def user_profile(request, user_id):
    user = User.objects.get(id=user_id)
    
    try:
        nickname = UserNickname.objects.get(user=user).nickname
    except UserNickname.DoesNotExist:
        nickname = random_nickname_generator()

    context = {
        'user': user,
        'nickname': nickname
    }
    return render(request, 'website/user_profile.html', context)

@login_required
def change_nickname(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        if nickname:
            user = request.user
            user_nickname, created = UserNickname.objects.get_or_create(user=user)
            user_nickname.nickname = nickname
            user_nickname.save()
            return redirect('website:user_profile', user_id=user.id)
    return redirect('website:user_profile', request.user.id)  # Redirect to a form page if GET request or no nickname provided

def random_nickname_generator():
    import random

    nicknames = [
    'RuneMaster', 'BladeOfDestiny', 'ShadowStriker', 'KnightOfValor', 'MysticMage', 
    'DragonSlayerX', 'ElvenArcher', 'DwarfSmith', 'NecroKnight', 'PhoenixRiderX', 
    'SilverSorcerer', 'WarlockLord', 'StormBringer', 'FrostKnight', 'DarkAssassin', 
    'FireWielder', 'ShadowHunter', 'IceMage', 'ThunderFist', 'GoldenWarrior', 
    'CrystalSeer', 'RuneWarrior', 'DragonTamer', 'ArcaneArcher', 'ShadowMage', 
    'SteelKnight', 'WindRider', 'BattleMage', 'GoblinCrusher', 'OrcBane', 
    'SilverRanger', 'RuneSlayer', 'MysticWarrior', 'DeathBringer', 'LightBearer', 
    'StormCaller', 'StoneGuardian', 'PhoenixKnight', 'DragonKnight', 'BladeDancer', 
    'IronClad', 'ShadowWalker', 'RuneHunter', 'StormWarrior', 'FlameWarden', 
    'RuneCraft', 'SpiritWalker', 'FireBlade', 'LightningStriker', 'IceRanger', 
    'RuneDefender', 'DuskMage', 'FrostGiant', 'StormWarden', 'ShadowFury', 
    'BladeMaster', 'WindWalker', 'RuneSentinel', 'StoneCrusher', 'IronGuard', 
    'PhoenixBlade', 'DragonWarden', 'ArcaneDefender', 'StormKnight', 'BlazeMage', 
    'RuneWarden', 'ShadowBlade', 'FrostWarden', 'LightningMage', 'WarriorMage', 
    'DarkRider', 'RuneWizard', 'DragonFury', 'ShadowKnight', 'StoneWarden', 
    'PhoenixWarden', 'IceKnight', 'StormRider', 'RuneBane', 'ShadowWizard', 
    'FlameKnight', 'LightningBlade', 'IronWarden', 'PhoenixMage', 'StormWizard', 
    'RuneWalker', 'FrostMage', 'BlazeKnight', 'ShadowWarden', 'RuneTamer', 
    'DragonWalker', 'WindKnight', 'IronMage', 'PhoenixRider', 'RuneRider', 
    'ShadowWalkerX', 'FrostKnightX', 'BlazeWarden', 'StormDefender', 'IronKnight'
    ]

    nickname = random.choice(nicknames) + str(random.randint(10,99))
    return nickname