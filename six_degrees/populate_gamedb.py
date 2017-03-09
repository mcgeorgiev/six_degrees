import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'game_test.settings')

import django
django.setup()
from game.models import Game, UserProfile

def populate():
    # First, we will create lists of dictionaries containing the pages
    # we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories.
    # This might seem a little bit confusing, but it allows us to iterate
    # through each data structure, and add the data to our models.

    game_one = [
        {"gameID": 1,
         "userID": 0000001,
         "source": "Scotland",
         "destination": "Australia",
         "numLinks": 10}
    ]

    user_one = [
        {"userName": "cam", "userID": 0000001, "password": "pw", "score": 10}
    ]

    # If you want to add more categories or pages,
    # add them to the dictionaries above.

    # The code below goes through the cats dictionary, then adds each category,
    # and then adds all the associated pages for that category.
    # if you are using Python 2.x then use cats.iteritems() see
    # http://docs.quantifiedcode.com/python-anti-patterns/readability/
    # for more information about how to iterate over a dictionary properly.

    for game, game_one in game_one.items():
        g = add_game(game)
#       # for p in cat_data["pages"]:
#       #     add_page(c, p["title"], p["url"])
#       c = add_cat(cat, cat_data["views"], cat_data["likes"])
#        for p in cat_data["pages"]:
#          add_page(c, p["title"], p["url"], p["views"])
#
#     # Print out the categories we have added.
    for g in Game.objects.all():
        print("- {0}".format(str(g)))
#
# def add_page(cat, title, url, views=0):
#     p = Page.objects.get_or_create(category=cat, title=title)[0]
#     p.url=url
#     p.views=views
#     p.save()
#     return p
#
def add_game(gameID, source, destination, userID=0000001, numLinks=10):
    g = Game.objects.get_or_create(gameID=gameID)[0]
    g.save()
    return g


# Start execution here!
if __name__ == '__main__':
    print("Starting Game population script...")
    populate()