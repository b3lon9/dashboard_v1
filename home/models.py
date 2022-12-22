from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser,BaseUserManager
from allauth.socialaccount.models import SocialAccount
from django.utils import timezone

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=30)
    year = models.CharField(max_length=5)
    population = models.PositiveIntegerField()

# word cloud용 DB
class Wordcloud(models.Model):
    text = models.CharField(max_length=30)
    value = models.PositiveIntegerField()
    
# Vote용 DB
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
    
class Vote(models.Model):
    choice = models.ForeignKey(Choice,on_delete=models.CASCADE)
    voter = models.ForeignKey(User,on_delete=models.CASCADE)

class User(models.Model):
    password = models.CharField(max_length=128)
    username = models.CharField(unique=True, max_length=150)
    last_name=models.CharField(max_length=150)
    phone = models.CharField(max_length=150)
    email=models.CharField(max_length=254,null=True)