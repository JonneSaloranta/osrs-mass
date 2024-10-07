from django.db import models
import requests
from bs4 import BeautifulSoup

class Quest(models.Model):
    difficulty = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    link = models.URLField()
    members = models.CharField(max_length=10)
    length = models.CharField(max_length=100)
    quest_points = models.IntegerField()
    series = models.CharField(max_length=100)

    def __str__(self):
        return self.name