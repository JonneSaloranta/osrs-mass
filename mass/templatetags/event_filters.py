from django import template
from django.utils.timezone import now
from django.utils.timesince import timeuntil
from django.utils.translation import gettext as _
from datetime import timedelta

register = template.Library()

@register.filter
def timeuntil_or_ongoing(start_date):
    if start_date <= now():
        return _("on going")
    return timeuntil(start_date)

@register.filter
def starts_in_10_minutes(start_date):
    return start_date <= now() + timedelta(minutes=10)

@register.filter
def is_in_progress(start_date, end_date):
    return start_date <= now() <= end_date

@register.filter
def is_upcoming(start_date):
    # Check if the event is upcoming (within 24 hours)
    return now() <= start_date <= now() + timedelta(hours=24)

@register.filter
def is_past(end_date):
    return end_date < now()