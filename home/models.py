from django.db import models

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=30)
    year = models.CharField(max_length=5)
    population = models.PositiveIntegerField()

# word cloud용 DB
class Wordcloud(models.Model):
    text = models.CharField(max_length=30)
    value = models.PositiveIntegerField()