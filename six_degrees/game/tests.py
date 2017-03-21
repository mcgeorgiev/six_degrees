from django.test import TestCase, Client
from models import *

# Create your tests here.

class TestAll(TestCase):
    def setUp(self):
        User.objects.create(username="testing",password="test")
        User.objects.create(username="tester",password="test")

    def test_user_added(self):
        user = User.objects.get(username="testing")
        self.assertEqual(user.username, "testing")

    def test_game_added(self):
        user = User.objects.get(username="testing")
        Game.objects.create(user=user,score=4,source="Dundee",destination="France",numLinks=4,bestLinks=2)
        gameT = Game.objects.get(user=user,score=4,source="Dundee")
        self.assertEqual(gameT.destination, "France")

    def test_game_change(self):
        user = User.objects.get(username="testing")
        Game.objects.create(user=user,score=4,source="Dundee",destination="France",numLinks=4,bestLinks=2)
        Game.objects.filter(user=user,score=4,source="Dundee").update(score=10)
        game = Game.objects.get(user=user,source="Dundee")
        self.assertEqual(game.score, 10)

class TestForms(TestCase):

    def test_login(self):
        c = Client()
        resp = c.post('/accounts/login/', {'username':'richard', 'password':'test'})
        self.assertEqual(resp.status_code, 200)

    def test_register(self):
        c = Client()
        resp = c.post('/accounts/register/', {'username':'test', 'password':'test', 'email':'test@t.com'})
        self.assertEqual(resp.status_code, 200)
