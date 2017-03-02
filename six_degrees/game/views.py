from django.shortcuts import render
from django.http import HttpResponse
from

def index(request):
    # Returns a rendered response to send to the client
    context_dict = {"something": "else"}
    response = render(request, 'game/index.html', context=context_dict)
    return response

# incoming
def incoming_node(request, title):
    return HttpResponse(title + "11111")


def player_selects_node(request):


    if has_enough_edges(current_node):
        get_related_nodes(current_node)
        # return the nodes to the front end
    else:
        add_API_nodes(current_node)
        # return nodes to the frontends
