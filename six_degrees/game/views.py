from django.shortcuts import render
from django.http import HttpResponse
import json
from graph import *
from django.views.decorators.csrf import csrf_exempt

def index(request):
    # Returns a starting node, related and end nodes
    return render(request, 'game/index.html', context={"a": "B"})

def get_start_node(request):
    data = nodes_with_num_relations(4)
    return HttpResponse(json.dumps(data))

# incoming
def incoming_node(request, title):

    current_node = {"name": title, "id": 0}
    if has_enough_edges(current_node):
        db_nodes = get_related_nodes(current_node)
    else:
        if not add_API_nodes(current_node):
            return HttpResponse(json.dumps({"code": 500, "status":"Failed"}))

        db_nodes = get_related_nodes(current_node)

    print db_nodes

    return HttpResponse(json.dumps(db_nodes))
    # # print data_back
    # # print type(data_back)

    # return HttpResponse(data_back)



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

    out = json.dumps(data)
    print out

def game_over(request):
    resp = request.POST.get('node')
    print resp
    print request.POST.get('csrfmiddlewaretoken')
    return HttpResponse()
