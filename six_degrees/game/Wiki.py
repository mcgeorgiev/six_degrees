import requests
import json
import sys
import random

def get_links_for(name, end):
    """ Returns a list of randomly chosen related links from the mediawiki API
        for a given article."""

    global all_links
    all_links = []
    # recursively get all the pages
    get_page(name)

    filtered_links = remove_meta_links(all_links)
    if filtered_links == []:
        return None

    # check if the end node exists in the filtered links
    end_node = None
    for i in range(0, len(filtered_links)):
        if filtered_links[i]["title"] == end:
            end_node = filtered_links[i]
            break

    # get a random selection of nine or less links from the thousands
    try:
        random_indexes = random.sample(range(0, len(filtered_links)), 9)
    except ValueError:
        random_indexes = random.sample(range(0, len(filtered_links)), len(filtered_links)-1)
    chosen_links = []
    for i in random_indexes:
        filtered_links[i]["title"].encode('utf-8')
        chosen_links.append(filtered_links[i])

    # add the end node
    if end_node:
        chosen_links.append(end_node)

    return chosen_links


def remove_meta_links(links):
    """Ensure all wikipedia meta links are removed"""
    for item in list(links):
        if item["ns"] != 0:
            links.remove(item)
    return links


def get_page(name, cont=""):
    """Recursive function to add all links for a page to all_links"""
    page_name = name
    link_limit = 500
    if cont != "":
        cont = "&plcontinue=" + cont

    api_url = u"https://en.wikipedia.org/w/api.php?action=query&titles={0}&prop=links&pllimit={1}&format=json&redirects=1{2}".format(page_name, link_limit, cont)

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
    print get_links_for("Glasgow", "Scotland")
