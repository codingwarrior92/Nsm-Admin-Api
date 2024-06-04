from django.db import models

# Create your models here.

class Keywords(models.Model):
    title = models.CharField(max_length=255)
    class Meta:
        db_table = 'keywords'