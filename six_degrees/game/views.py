from __future__ import division
from django.shortcuts import render
from django.http import HttpResponse
#from Wiki import get_page_links
from models import UserProfile
from django.contrib.auth.models import User
from models import Game
from django.contrib.auth.decorators import login_required
from forms import UserProfileForm
from django.shortcuts import redirect
from django.db.models import Count, Avg

import json
from graph import *
from django.views.decorators.csrf import csrf_exempt

@login_required
def index(request):
    # Returns a starting node, related and end nodes
    return render(request, 'game/index.html', context={"a": "B"})

def scores(request):
    score_list = Game.objects.order_by('-score')[:50]
    context = {'score_list': score_list,}
    for gme in score_list:
        gme.score = gme.score * 100
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
def tutorial(request):
    return render(request, 'game/tutorial.html')

@login_required
def dashboard(request):
    user = User.objects.get(username=request.user.username)
    score_list = Game.objects.all().filter(user=user).order_by('-score')[:100]
    #profile = UserProfile.objects.all().get(user=user)
    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    # form = UserProfileForm(
    #     {'picture': userprofile.picture})
    #
    # if request.method == 'POST':
    #     form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
    #     if form.is_valid():
    #         form.save(commit=True)
    #         return redirect('profile', user.username)
    #     else:
    #         print(form.errors)
    # return render(request, 'game/dashboard.html',
    #     {'userprofile': userprofile, 'selecteduser': user, 'form': form})
    try:
        best_score = score_list.first().score * 100
        for gme in score_list:
            gme.score = gme.score * 100

        user_sc = userprofile.score * 100
        print user_sc
        context = {'score_list': score_list, 'best_score': best_score, 'profile': userprofile, 'user_score':user_sc}
        return render(request, 'game/dashboard.html', context)
    except:
        return render(request, 'game/dashboard.html')

def get_start_node(request):
    data = get_start_data()
    return HttpResponse(json.dumps(data))


def incoming_node(request, title):
    end_name = request.POST["endNode"]
    current_node = {"name": title, "id": 0}
    if has_enough_edges(current_node):
        # get the existing edges first and then fill up with the others
        pass
    else:
        if not add_API_nodes(current_node, end_name):
            return HttpResponse(json.dumps({"code": 500, "status":"Failed"}))

    db_nodes = get_related_nodes(current_node)
    #print db_nodes

    print "Number of all the nodes returned:" + str(len(db_nodes))

    if len(db_nodes) >= 16:
        db_nodes = remove_some_nodes(db_nodes, end_name)

    return HttpResponse(json.dumps(db_nodes))


def remove_some_nodes(nodes, end_name):
    end_node = None
    for i in range(0, (len(nodes) - 1)):
        if end_name in nodes[i].values():
            end_node = nodes.pop(i)

    smaller_nodes = nodes[:15]
    if end_node != None:
        smaller_nodes.append(end_node)
    return smaller_nodes


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

def register_profile(request):
    form = UserProfileForm()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
           # user_profile.user = request.user
            user_profile.save()
            return redirect('index')
        else:
            print(form.errors)
    context_dict = {'form':form}
    return render(request, 'game/profile_registration.html', context_dict)


#@csrf_exempt
def game_over(request):
    data = request.POST
    print "[[][][]]"

    nodes = json.loads(data["nodes"])

    source = nodes[0]
    if data["lost"] == "False":
        destination = nodes[-1]
        shortest_path = get_shortest_path(source["label"], destination["label"])

        if len(shortest_path) == len(nodes):
            shortest_path = [node["label"] for node in nodes]
            print "you got the shortest_path"

        user_score =  (len(shortest_path) - 1) / (len(nodes) - 1)
        print user_score
        if user_score > 1:
            user_score = 1
        user = User.objects.get(username=request.user.username)
        Game.objects.create(user=user,
                            score=user_score,
                            source=str(source['label']),
                            destination=str(destination['label']),
                            numLinks=len(nodes)-1,
                            bestLinks=len(shortest_path)-1)

        # calculate the users new overall score
        user_overall_sc = Game.objects.filter(user=user).aggregate(score=Avg('score'))['score']
        print "score"
        print user_overall_sc

        userprofile = UserProfile.objects.get_or_create(user=user)[0]

        userprofile.score = user_overall_sc
        print userprofile.score
        userprofile.save()

        # gets the last entry for a user and adds it to the graph db
        game = Game.objects.filter(user=user).latest('id')
        add_game_relationship(nodes, game.id)

    else:
        shortest_path = get_shortest_path(source["label"], data["end"])

    shortest_path_nodes = []
    for item in shortest_path:
        shortest_path_nodes.append({"label": item})
    return HttpResponse(json.dumps(shortest_path_nodes))


    if __name__=='__main__':
        game_over('')
