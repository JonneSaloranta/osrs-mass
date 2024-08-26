from django.db import models
import time
import uuid
class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, blank=True)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    invite_code = models.CharField(max_length=6, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = self.generate_invite_code()
        super(Event, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return f'/details/{self.uuid}'
    

    def generate_invite_code(self):
        import random
        import string
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))