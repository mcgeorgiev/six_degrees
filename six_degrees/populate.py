import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'game_test.settings')
import django
django.setup()
#from game.models import Game, UserProfile
from django.contrib.auth.models import User
from game.models import Game

def populate():

    user_one = [
        user
    ]

    me=User.objects.get(username='Admin1')
    game_one = [
        user = me
        score = 10
        source = 'Testing Source'
        destination = 'Testing Destination'
        numLinks = 15
        bestLinks = 5
    ]

    me=User.objects.get(username='Admin2')
    game_two = [
        user = me
        score = 11
        source = 'Testing Source2'
        destination = 'Testing Destination2'
        numLinks = 17
        bestLinks = 6
    ]

