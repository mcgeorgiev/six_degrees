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
    score_list = Game.objects.order_by('-score')[:100]
    context = {'score_list': score_list,}
    return render(request, 'game/scores.html', context)

# def scores(request):
#     score_list = UserProfile.objects.order_by('score')[:100]
#     context_dict = {'userprofiles': score_list}
#     return render(request, 'game/scores.html', context_dict)

def rules(request):
    return render(request, 'game/rules.html')

def home(request):
    return render(request, 'game/home.html')

@login_required
def dashboard(request):
    user = User.objects.get(username=request.user.username)
    score_list = Game.objects.all().filter(user=user).order_by('-score')[:100]
    best_score = score_list.last().score
    context = {'score_list': score_list, 'best_score': best_score}
    return render(request, 'game/dashboard.html', context)

def get_start_node(request):
    data = nodes_with_num_relations(4)
    return HttpResponse(json.dumps(data))


def incoming_node(request, title):
    print request.POST["endNode[name]"]
    current_node = {"name": title, "id": 0}
    if has_enough_edges(current_node):
        # get the existing edges first and then fill up with the others
        pass
    else:
        if not add_API_nodes(current_node):
            return HttpResponse(json.dumps({"code": 500, "status":"Failed"}))

    db_nodes = get_related_nodes(current_node)

    print "Number of all the nodes returned:" + str(len(db_nodes))

    return HttpResponse(json.dumps(db_nodes))


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


#@csrf_exempt
def game_over(request):
    data = request.POST
    nodes = json.loads(data["nodes"])

    source = nodes[0]
    destination = nodes[-1]
    shortest_path = get_shortest_path(source["label"], destination["label"])

    if len(shortest_path) == len(nodes):
        shortest_path = [node["label"] for node in nodes]
        print "you got the shortest_path"

    user = User.objects.get(username=request.user.username)
    Game.objects.create(user=user,
                        score=21,
                        source=str(source['label']),
                        destination=str(destination['label']),
                        numLinks=len(nodes)-1,
                        bestLinks=len(shortest_path)-1)

    # gets the last entry for a user and adds it to the graph db
    game = Game.objects.filter(user=user).latest('id')
    add_game_relationship(nodes, game.id)

    shortest_path_nodes = []
    for item in shortest_path:
        shortest_path_nodes.append({"label": item})
    print shortest_path_nodes
    return HttpResponse(json.dumps(shortest_path_nodes))


    if __name__=='__main__':
        game_over('')
