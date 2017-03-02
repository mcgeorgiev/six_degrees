from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    # Returns a rendered response to send to the client
    context_dict = {"something": "else"}
    response = render(request, 'game/index.html', context=context_dict)

    return response
