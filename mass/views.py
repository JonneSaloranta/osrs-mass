from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone

from .models import Event, InviteUsage

def index(request):
    all_events = Event.objects.all()

    context = {
        'events': all_events
    }
    return render(request, 'mass/index.html', context=context)

def create(request):
    return render(request, 'mass/create_event.html')

def update(request):
    return render(request, 'mass/update_event.html')

def delete(request):
    return render(request, 'mass/index.html')

from django.shortcuts import render

def join(request):
    invite_code = request.GET.get('invite_code')
    
    if invite_code:
        # Retrieve the event using the invite code
        event = get_object_or_404(Event, invite_code=invite_code)

        # Identify the user, either by session key or IP address
        user_id = request.session.session_key or request.META.get('REMOTE_ADDR')

        # Get or create an InviteUsage record for this invite code and user
        invite_usage, created = InviteUsage.objects.get_or_create(invite_code=invite_code, user_id=user_id)

        # Check if the invite code usage is still valid (within 24 hours)
        if invite_usage.is_valid():
            # Update the last used timestamp
            invite_usage.last_used = timezone.now()
            invite_usage.save()

            # If valid, pass the event to the context
            context = {
                'event': event
            }

            # Render the event details page
            return render(request, 'mass/details_event.html', context=context)
        else:
            # If the invite code is expired, show an error
            context = {
                'error': 'Your invite code has expired. Please request a new one.'
            }
    else:
        # If no invite code is provided or it doesn't exist, show an error
        context = {
            'error': 'Invalid invite code'
        }

    # Render the index page with the error context
    return render(request, 'mass/index.html', context=context)

def leave(request):
    return render(request, 'mass/index.html')

def details(request, id):
    event = get_object_or_404(Event, pk=id)
    context = {
        'event': event
    }
    return render(request, 'mass/details_event.html' , context=context)

