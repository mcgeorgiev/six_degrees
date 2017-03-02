from django.shortcuts import render
from django.http import HttpResponse
from Wiki import get_page_links
import json
from graph import *

def index(request):
    # Returns a rendered response to send to the client
    context_dict = {"something": "else"}
    response = render(request, 'game/index.html', context=context_dict)
    return response


# incoming
def incoming_node(request, title):
    data_back = get_page_links(title)
    # print data_back
    # print type(data_back)

    return HttpResponse(data_back)


def incoming_node(request, name):
    current_node = {"name": name, "id": 0}

    if has_enough_edges(current_node):
        db_nodes = get_related_nodes(current_node)
    else:
        db_nodes = add_API_nodes(current_node)

    return HttpResponse(convert_for_sigma(current_node, db_nodes))


def convert_for_sigma(current_node, all_nodes):
    # build json response with all current nodes
    data = {}
    data["nodes"] = [{"id":"n0", "label":current_node["name"], "x":0, "y":0, "size":2}]
    data["edges"] = []

    counter = count(1)

    all_links = []
    for links in all_nodes:
        node_id = counter.next()
        data["nodes"] += {"id":"n{0}".format(node_id),
                        "label":links['name'],
                        "size":1,
                        "x":node_id,
                        "y":node_id},
        # and edges between nodes
        data["edges"] += {"id":"e{0}".format(node_id),
                        "source":"n0",
                        "target":"n{0}".format(node_id)},
    return data
