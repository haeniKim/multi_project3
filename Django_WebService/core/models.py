from django.db import models

# Create your models here.
class Snack(models.Model):
    name = models.CharField(max_length=50)
    info = models.CharField(max_length=200)
    price = models.IntegerField(default=0)