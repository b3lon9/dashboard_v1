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

class UserManager(BaseUserManager):
    def create_user(self,username,password,last_name,email,phone,date_of_birth):
        user = self.model(
            username=username,
            last_name=last_name,
            email=self.normalize_email(email),
            phone=phone,
            date_of_birth=date_of_birth,
            date_joined=timezone.now(),
            is_superuser=0,
            is_staff=0,
            is_active = 1
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_super(self,username,last_name,email,phone,date_of_birth,password):
        user=self.create_user(
            username=username,
            password=password,
            last_name = last_name,
            email=email,
            phone=phone,
            date_of_birth=date_of_birth
        )
        user.is_superuser=1
        user.is_staff=1
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    password = models.CharField(max_length=128)
    username = models.CharField(unique=True, max_length=150)
    is_superuer = models.IntegerField()
    last_name=models.CharField(max_length=150)
    phone = models.CharField(max_length=150)
    email=models.CharField(max_length=254,null=True)
    date_of_birth = models.DateTimeField(null=True)
    date_joined = models.DateTimeField()
    last_login = models.DateTimeField(blank=True,null=True)
    is_staff = models.IntegerField(blank=True,null=True)
    is_active = models.IntegerField(blank=True,null=True)
    first_name = models.CharField(max_length=30,blank=True,null=True)
    
    object = UserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS= ['last_name','phone','email','date_of_birth']
    
    def has_perm(self,perm,obj=None):
        return True
    
    def has_module_perms(self,app_label):
        return True
    
    class Meta:
        db_table='User'
