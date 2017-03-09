import requests
import json
from itertools import count
import sys
import random

def get_links_for(name):
    global all_links
    all_links = []
    get_page(name)

    filtered_links = remove_meta_links(all_links)
    print len(filtered_links)
    try:
        random_indexes = random.sample(range(0, len(filtered_links)), 10)
    except ValueError:
        random_indexes = random.sample(range(0, len(filtered_links)), len(filtered_links)-1)
    chosen_links = []
    for i in random_indexes:
        filtered_links[i]["title"].encode('utf-8')
        chosen_links.append(filtered_links[i])
    return chosen_links


def remove_meta_links(links):
    for item in list(links):
        if item["ns"] != 0:
            links.remove(item)
    return links

# page id to get links currently all links from "broughty ferry" page
def get_page(name, cont=""):
    page_name = name
    link_limit = 500
    if cont != "":
        cont = "&plcontinue=" + cont

    api_url = "https://en.wikipedia.org/w/api.php?action=query&titles={0}&prop=links&pllimit={1}&format=json&redirects=1{2}".format(page_name, link_limit, cont)

    r = requests.get(api_url)
    resp = r.json()

    for nested_json in resp["query"]["pages"]:
        page_id = nested_json

    if page_id == "-1":
        return None

    raw_links = resp["query"]["pages"]["{0}".format(page_id)]["links"]

    for item in raw_links:
        all_links.append(item)

    if "batchcomplete" in resp:
        return
    else:
        return get_page(name, resp["continue"]["plcontinue"])


if __name__ == '__main__':
    get_links_for("Glasgow")
    # wiki = Wikipedia()
    # print len(wiki.get_links("Australia"))
