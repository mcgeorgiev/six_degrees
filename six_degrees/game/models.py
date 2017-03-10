from __future__ import unicode_literals
from django.db import models
#from django.contrib.auth.models import User

# Create your models here.
class Game(models.Model):
    gameID = models.IntegerField(unique=True)
    username = models.CharField(max_length=128)
    userID = models.IntegerField(unique=True)
    source = models.CharField(max_length=128)
    destination = models.CharField(max_length=128)
    numLinks = models.IntegerField()

    class Meta:
        verbose_name_plural = 'games'

    def __unicode__(self):
        return self.username

class UserProfile(models.Model):
    username = models.CharField(max_length=128)
    userID = models.IntegerField(unique=True)
    password = models.CharField(max_length=128)
    score = models.IntegerField()

    class Meta:
        verbose_name_plural = 'userprofiles'

    def __unicode__(self):
        return self.username


# class UserProfile(models.Model):
#     user = models.OneToOneField(User)
#     website = models.URLField(blank=True)
#     picture = models.ImageField(upload_to='profile_images', blank=True)
#     score = models.IntegerField()
#
#     def __unicode__(self):
#         return self.user.username

