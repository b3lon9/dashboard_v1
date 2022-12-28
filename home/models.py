from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, AbstractBaseUser,BaseUserManager
from allauth.socialaccount.models import SocialAccount
from django.utils import timezone

# word cloud용 DB
class Wordcloud(models.Model):
    text = models.CharField(max_length=30)
    value = models.PositiveIntegerField()

class Community(models.Model):
    uid = models.CharField(max_length=150)
    key1 = models.CharField(max_length=128)
    key2 = models.CharField(max_length=128)
    cur_key = models.CharField(max_length=128)
    text = models.CharField(max_length=1024)
    
class UserEtc(models.Model):
    user_id = models.CharField(max_length=150)
    user_img = models.ImageField(upload_to='images/')
    user_rd = models.DateTimeField(null=True)
    
    def __str__(self):
        return self.user_id