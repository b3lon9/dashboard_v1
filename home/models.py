from django.db import models

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=30)
    year = models.CharField(max_length=5)
    population = models.PositiveIntegerField()