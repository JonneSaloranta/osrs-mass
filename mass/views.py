from django.shortcuts import render 
from django.shortcuts import get_object_or_404

from .models import Event

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

def join(request):
    return render(request, 'mass/index.html')

def leave(request):
    return render(request, 'mass/index.html')

def details(request, id):
    event = get_object_or_404(Event, pk=id)
    context = {
        'event': event
    }
    return render(request, 'mass/datails_event.html' , context=context)

