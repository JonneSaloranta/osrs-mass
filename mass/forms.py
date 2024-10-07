from django import forms
from .models import Event, Requirement
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import datetime

class EventForm(forms.ModelForm):
    start_date = forms.DateField(
        initial=timezone.now().date(),
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    start_time = forms.TimeField(
        initial=timezone.now().time(),
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'})
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    end_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'})
    )
    
    requirements = forms.ModelMultipleChoiceField(
        queryset=Requirement.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    
    class Meta:
        model = Event
        fields = ['name', 'description', 'start_date', 'start_time', 'end_date', 'end_time', 'location', 'requirements', 'event_image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Event Description'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'event_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        start_time = cleaned_data.get('start_time')
        end_date = cleaned_data.get('end_date')
        end_time = cleaned_data.get('end_time')
        
        if start_date and start_time:
            cleaned_data['start_date'] = datetime.datetime.combine(start_date, start_time)
        
        if end_date and end_time:
            cleaned_data['end_date'] = datetime.datetime.combine(end_date, end_time)
        
        return cleaned_data
