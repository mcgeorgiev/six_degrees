from django.shortcuts import render
from django.http import HttpResponse
from Wiki import get_page_links
from django.views.decorators.clickjacking import xframe_options_sameorigin
import json

def index(request):
    # Returns a rendered response to send to the client
    context_dict = {"something": "else"}
    response = render(request, 'game/index.html', context=context_dict)
    return response

# incoming
@xframe_options_sameorigin
def incoming_node(request, title):
    data_back = get_page_links(title)
    print type(data_back)
    data_back = json.dumps(data_back)
    print type(data_back)
    print data_back

    return data_back
