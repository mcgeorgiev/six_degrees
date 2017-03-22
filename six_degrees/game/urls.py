from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.game, name='game'),
	url(r'^incomingnode/((?P<title>.*))/$', views.incoming_node, name='incoming_node'),
	url(r'^start/$', views.get_start_node, name='get_start_node'),
	url(r'^gameover/$', views.game_over, name='game_over'),
	url(r'^tutorial/$', views.tutorial, name='tutorial')
]
