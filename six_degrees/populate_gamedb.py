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

    # If you want to add more catergories or pages,
    # add them to the dictionaries above.

    # The code below goes through the cats dictionary, then adds each category,
    # and then adds all the associated pages for that category.
    # if you are using Python 2.x then use cats.iteritems() see
    # http://docs.quantifiedcode.com/python-anti-patterns/readability/
    # for more information about how to iterate over a dictionary properly.

#     for cat, cat_data in cats.items():
#         # c = add_cat(cat)
#         # for p in cat_data["pages"]:
#         #     add_page(c, p["title"], p["url"])
#         c = add_cat(cat, cat_data["views"], cat_data["likes"])
#         for p in cat_data["pages"]:
#             add_page(c, p["title"], p["url"], p["views"])
#
#     # Print out the categories we have added.
#     for c in Category.objects.all():
#         for p in Page.objects.filter(category=c):
#             print("- {0} - {1}".format(str(c), str(p)))
#
# def add_page(cat, title, url, views=0):
#     p = Page.objects.get_or_create(category=cat, title=title)[0]
#     p.url=url
#     p.views=views
#     p.save()
#     return p
#
# def add_cat(name, views=0, likes=0):
#     c = Category.objects.get_or_create(name=name)[0]
#     c.views=views
#     c.likes=likes
#     c.save()
#     return c

# Start execution here!
if __name__ == '__main__':
    print("Starting Game population script...")
    populate()