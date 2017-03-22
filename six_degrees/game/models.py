from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Represents a user's profile details"""

    user = models.OneToOneField(User, null=True)
    score = models.DecimalField(decimal_places=2, max_digits=4, default=0.0, editable=True)

    class Meta:
      verbose_name_plural = 'userprofiles'

    def __unicode__(self):
      return self.user.username

    def __str__(self):
      return self.user


class Game(models.Model):
    """Represents a game a user has played."""

    user = models.ForeignKey('auth.User')
    score = models.DecimalField(decimal_places=2, max_digits=5, null=True)
    source = models.CharField(max_length=128)
    destination = models.CharField(max_length=128)
    numLinks = models.IntegerField(null=True)
    bestLinks = models.IntegerField(null=True)

    class Meta:
        verbose_name_plural = 'games'
