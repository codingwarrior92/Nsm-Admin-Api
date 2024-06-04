from django.db import models

# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=255)
    twitter_id = models.CharField(max_length=255, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    telegram_id = models.CharField(max_length=255, null=True, blank=True)
    twitter_followers = models.IntegerField(default=0)
    telegram_subscribers = models.IntegerField(default=0)
    class Meta:
        db_table = 'client'