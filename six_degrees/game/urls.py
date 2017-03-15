from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^scores/', views.scores, name='scores'),
	url(r'^incomingnode/((?P<title>.*))/$', views.incoming_node, name='incoming_node'),
	url(r'^start/$', views.get_start_node, name='get_start_node'),
	url(r'^gameover/$', views.game_over, name='game_over'),
	url(r'^dashboard/$', views.dashboard, name='dashboard')
]
