from django.db import models

# Create your models here.

class Crypto(models.Model):
    coin_id = models.CharField(max_length=255)
    class Meta:
        db_table = 'crypto'

class CoinProfile(models.Model):
    coin_id = models.CharField(max_length=255)
    balance = models.CharField(max_length=255)
    twitter_followers = models.IntegerField(default=0)
    tg_subscribers = models.IntegerField(default=0)
    class Meta:
        db_table = 'coin_profile'

class CoinHistorical(models.Model):
    coin_id = models.CharField(max_length=255)
    balance = models.CharField(max_length=255)
    twitter_followers = models.IntegerField(default=0)
    tg_subscribers = models.IntegerField(default=0)
    class Meta:
        db_table = 'coin_historical'