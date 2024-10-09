from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from email_login.models import User

class InviteUsage(models.Model):
    invite_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)  # New field to track when the invite code was created
    last_used = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invite_usages')  # Changed to ForeignKey

    def is_valid(self):
        return timezone.now() <= self.last_used + timedelta(days=7)  # Valid for 7 days

    def __str__(self):
        return f'{self.invite_code} - {self.user}'

class Requirement(models.Model):
    QUEST = 'quest'
    SKILL = 'skill'
    OTHER = 'other'

    REQUIREMENT_TYPES = [
        (QUEST, 'Quest'),
        (SKILL, 'Skill'),
        (OTHER, 'Other'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=10, choices=REQUIREMENT_TYPES, default=OTHER)
    required_level = models.PositiveIntegerField(blank=True, null=True)  # Optional, but consider adding validation for it
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='sub_requirements', blank=True, null=True)
    wiki_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

class Event(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, blank=True)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    invite_code = models.CharField(max_length=6, unique=True, blank=True, null=True)
    requirements = models.ManyToManyField(Requirement, blank=True, related_name='events')
    event_image = models.ImageField(upload_to='event_images/', blank=True, null=True)

    def __str__(self):
        return f'{self.name} - {self.invite_code}'

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = self.generate_invite_code()

        # Check for existing image to delete
        if self.pk:  # Only if the object is already saved
            existing = Event.objects.filter(id=self.pk).first()
            if existing and existing.event_image and existing.event_image != self.event_image:
                existing.event_image.delete(save=False)

        super(Event, self).save(*args, **kwargs)

    @receiver(models.signals.pre_delete, sender='mass.Event')
    def server_delete_event_image(sender, instance, **kwargs):
        if instance.event_image:
            instance.event_image.delete(save=False)

    def get_absolute_url(self):
        return f'/details/{self.uuid}'

    @property
    def get_event_image_url(self):
        if self.event_image:
            return self.event_image.url
        return 'https://placehold.co/600x400?text=No%20\nImage'

    def generate_invite_code(self):
        import random
        import string
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
