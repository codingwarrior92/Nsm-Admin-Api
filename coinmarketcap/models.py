from django.db import models

# Create your models here.

class Crypto(models.Model):
    coin_id = models.IntegerField()
    class Meta:
        db_table = 'crypto'