from django.test import TestCase, Client
from models import *

class TestGameUser(TestCase):

    def setUp(self):
        """ Set up users to test """

        User.objects.create(username="testing",password="test")
        User.objects.create(username="tester",password="test")
        print 'Setting up - adding users'


    def test_user_added(self):
        """Test a user has been added"""

        print 'Testing user added'
        user = User.objects.get(username="testing")
        self.assertEqual(user.username, "testing")


    def test_game_added(self):
        """ Test a played game has been added."""

        print 'Testing game added'
        user = User.objects.get(username="testing")
        Game.objects.create(user=user,score=4,source="Dundee",destination="France",numLinks=4,bestLinks=2)
        gameT = Game.objects.get(user=user,score=4,source="Dundee")
        self.assertEqual(gameT.destination, "France")


    def test_game_change(self):
        """ Test a game has been updated."""

        print 'Testing game change'
        user = User.objects.get(username="testing")
        Game.objects.create(user=user,score=4,source="Dundee",destination="France",numLinks=4,bestLinks=2)
        Game.objects.filter(user=user,score=4,source="Dundee").update(score=10)
        game = Game.objects.get(user=user,source="Dundee")
        self.assertEqual(game.score, 10)


class TestForms(TestCase):

    def test_login(self):
        """ Test the login functionality """

        print 'Testing login works'
        c = Client()
        resp = c.post('/accounts/login/', {'username':'richard', 'password':'test'})
        self.assertEqual(resp.status_code, 200)


    def test_register(self):
        """ Test the registration functionality """

        print 'Testing registration page works'
        c = Client()
        resp = c.post('/accounts/register/', {'username':'test', 'password':'test', 'email':'test@t.com'})
        self.assertEqual(resp.status_code, 200)


class TestViews(TestCase):

    def test_game_notlogged(self):
        """ Test that pages are restricted if not logged in."""
        
        print 'Testing game page is restricted'
        c = Client()
        resp = c.get('/game/')
        self.assertEqual(resp.status_code, 302)
