from django.shortcuts import render
from django.http import HttpResponse
#from Wiki import get_page_links
from models import UserProfile
from django.contrib.auth.models import User
from models import Game
from django.contrib.auth.decorators import login_required

import json
from graph import *
from django.views.decorators.csrf import csrf_exempt

@login_required
def index(request):
    # Returns a starting node, related and end nodes
    return render(request, 'game/index.html', context={"a": "B"})

def scores(request):
    score_list = UserProfile.objects.order_by('score')[:100]
    context_dict = {'userprofiles': score_list}
    return render(request, 'game/scores.html', context_dict)

def rules(request):
    return render(request, 'game/rules.html')

def home(request):
    return render(request, 'game/home.html')




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
    #resp = request.POST
    #resp = resp.json()
    #print resp
    # for x in resp:
    #     print x["nodes"]["label"]
   # print request.POST.get('csrfmiddlewaretoken')

    #return HttpResponse()

    me=User.objects.get(username='Cam5')
    Game.objects.create(user=me, score=21, source='Scotland', destination='England', numLinks=19, bestLinks=8)
    g=Game.objects.all()
    l=g[len(g)-1]
    print l.user, l.score, l.source, l.destination, l.numLinks, l.bestLinks

    if __name__=='__main__':
        game_over('')

