import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'game_test.settings')
import django
django.setup()
from game.models import Game, UserProfile
from django.contrib.auth.models import User

def populate():

    users = [
        {"user": "Alice", "password": "pw", "email": "Alice@sixdegrees.com", "userscore": 0.62},
        {"user": "Bob", "password": "pw", "email": "Bob@sixdegrees.com", "userscore": 0.82},
        {"user": "Carol", "password": "pw", "email": "Carol@sixdegrees.com", "userscore": 0.26},
        {"user": "Dennis", "password": "pw", "email": "Dennis@sixdegrees.com", "userscore": 0.76},
        {"user": "Elaine", "password": "pw", "email": "Elaine@sixdegrees.com", "userscore": 0.63},
        {"user": "Frank", "password": "pw", "email": "Frank@sixdegrees.com", "userscore": 0.47},
    ]
    games = [
        {"score": 0.5, "source": "Milky Way", "destination": "Satellite", "numLinks": 4, "bestLinks": 2},
        {"score": 0.5, "source": "Beijing", "destination": "Consciousness", "numLinks": 6, "bestLinks": 3},
        {"score": 0.67, "source": "Arctic", "destination": "Mumbai", "numLinks": 3, "bestLinks": 2},
        {"score": 0.5, "source": "Arctic", "destination": "Mumbai", "numLinks": 4, "bestLinks": 2},
        {"score": 1.0, "source": "Age of Enlightenment", "destination": "Agriculture", "numLinks": 2, "bestLinks": 2},
        {"score": 0.75, "source": "Silicon", "destination": "History of Science", "numLinks": 4, "bestLinks": 3},
        {"score": 0.43, "source": "Mississippi River", "destination": "Big Bang", "numLinks": 7, "bestLinks": 3},
        {"score": 0.4, "source": "Economics", "destination": "Upanishads", "numLinks": 5, "bestLinks": 2},
        {"score": 0.67, "source": "Werner Heisenberg", "destination": "Carbon", "numLinks": 3, "bestLinks": 2},
        {"score": 1.0, "source": "Metaphysics", "destination": "Space Exploration", "numLinks": 2, "bestLinks": 2},
        {"score": 1.0, "source": "Science", "destination": "Jainism", "numLinks": 2, "bestLinks": 2},
        {"score": 0.67, "source": "Mass media", "destination": "History of Earth", "numLinks": 3, "bestLinks": 2},
        {"score": 0.33, "source": "Printing", "destination": "Aesthetics", "numLinks": 6, "bestLinks": 2},
    ]



    for user in users:
        add_user(user["user"], user["password"], user["email"])
        u=User.objects.get(username=user["user"])
        up=add_userprofile(u,user["userscore"])
        for game in games:
            g=add_game(u, game)


def add_user(name, password, email):
    u = User.objects.create(username=name,password=password, email=email)
  #  u.email=email
  #  u.score=userscore
    u.save()
    return u

def add_userprofile(user, score):
    userprofile = UserProfile.objects.create(user=user, score=score)
    userprofile.save()

def add_game(user, game):
    g = Game.objects.create(user=user)
    g.score=game["score"]
    g.source=game["source"]
    g.destination=game["destination"]
    g.numLinks=game["numLinks"]
    g.bestLinks=game["bestLinks"]
    g.save()
   # return g

# Start execution here!
if __name__ == '__main__':
    print("Starting SixDegrees Django population script...")
    populate()