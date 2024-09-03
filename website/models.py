from django.db import models

from email_login.models import User

class UserNickname(models.Model):
    nickname = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nickname