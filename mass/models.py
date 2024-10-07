from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from email_login.models import User

class InviteUsage(models.Model):
    invite_code = models.CharField(max_length=6)
    last_used = models.DateTimeField(default=timezone.now)
    user_id = models.CharField(max_length=255)  # You can use IP, session key, or user ID

    def is_valid(self):
        return timezone.now() <= self.last_used + timedelta(hours=24*7)
    
    def __str__(self):
        return f'{self.invite_code} - {self.user_id}'
    
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
    required_level = models.PositiveIntegerField(blank=True, null=True)
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
    requirements = models.ManyToManyField(Requirement, blank=True, related_name='requirements')
    event_image = models.ImageField(upload_to='event_images/', blank=True, null=True)

    def __str__(self):
        return f'{self.name} - {self.invite_code}'
    
    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = self.generate_invite_code()
        
        if self.id:
            existing = get_object_or_404(Event, id=self.id)
            if existing.event_image:
                if existing.event_image != self.event_image:
                    existing.event_image.delete(save=False)
        
        super(Event, self).save(*args, **kwargs)

        @receiver(models.signals.pre_delete, sender="mass.Event")
        def server_delete_event_image(sender, instance, **kwargs):
            for field in instance._meta.fields:
                if field.name == 'event_image':
                    file = getattr(instance, field.name)
                    if file:
                        file.delete(save=False)

    def get_absolute_url(self):
        return f'/details/{self.uuid}'
    
    def get_event_image_url(self):
        if self.event_image:
            return self.event_image.url
        return 'https://via.placeholder.com/150'

    def generate_invite_code(self):
        import random
        import string
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    