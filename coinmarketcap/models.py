from django.db import models

# Create your models here.

class Crypto(models.Model):
    coin_id = models.CharField(max_length=255)
    class Meta:
        db_table = 'crypto'

class CoinProfile(models.Model):
    coin_id = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    weburl = models.CharField(default='', max_length=255)
    twitter = models.CharField(default='', max_length=255)
    telegram = models.CharField(default='',max_length=255)
    class Meta:
        db_table = 'coin_profile'

class CoinPriceHistorical(models.Model):
    coin_id = models.CharField(max_length=255)
    price = models.CharField(max_length=255, null=True)
    timestamp = models.IntegerField(default=0)
    class Meta:
        db_table = 'coin_price_historical'