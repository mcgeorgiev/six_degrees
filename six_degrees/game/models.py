from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
  #  username = models.CharField(max_length=128)
   # userID = models.IntegerField(unique=True)
   # password = models.CharField(max_length=128)
    user = models.OneToOneField(User, null=True)
    picture = models.ImageField(upload_to='media', blank=True)
    score = models.DecimalField(decimal_places=2, max_digits=4, default=0.0, editable=True)

    class Meta:
      verbose_name_plural = 'userprofiles'

    def __unicode__(self):
      return self.user.username

    def __str__(self):
      return self.user



# Create your models here.
class Game(models.Model):
   # gameID = models.IntegerField(unique=True)
   # username = models.CharField(max_length=128)
    user = models.ForeignKey('auth.User')
    score = models.DecimalField(decimal_places=2, max_digits=5, null=True)
    source = models.CharField(max_length=128)
    destination = models.CharField(max_length=128)
    numLinks = models.IntegerField(null=True)
    bestLinks = models.IntegerField(null=True)

    class Meta:
        verbose_name_plural = 'games'
    #
    # def __unicode__(self):
    #     return self.user

# class UserProfile(models.Model):
#     user = models.OneToOneField(User)
#     website = models.URLField(blank=True)
#     picture = models.ImageField(upload_to='profile_images', blank=True)
#     score = models.IntegerField()
#
#     def __unicode__(self):
#         return self.user.username
