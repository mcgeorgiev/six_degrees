from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^incomingnode/((?P<title>.*))/$', views.incoming_node, name='incoming_node'),

]
