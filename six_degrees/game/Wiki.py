import requests
import json
from itertools import count
import sys
# page id to get links currently all links from "broughty ferry" page
def get_page_links(name):
    page_name = name
    link_limit = 10

    api_url = "https://en.wikipedia.org/w/api.php?action=query&titles={0}&prop=links&pllimit={1}&format=json".format(page_name, link_limit)

    r = requests.get(api_url)
    resp = r.json()
    print resp
    #page_id = resp['query']['pages']['360393']['pageid']
    for nested_json in resp["query"]["pages"]:
        page_id = nested_json

    if page_id == "-1":
        return None

    # build json response with all current nodes
    data = {}
    data["nodes"] = [{"id":"n0", "label":resp["query"]["pages"]["{0}".format(page_id)]["title"], "x":0, "y":0, "size":2}]
    data["edges"] = []

    counter = count(1)

    all_links = []

    for links in resp["query"]["pages"]["{0}".format(page_id)]["links"]:
        # create json for this pages links
        # node_id = counter.next()
        # data["nodes"] += {"id":"n{0}".format(node_id),
        #                 "label":links['title'],
        #                 "size":1,
        #                 "x":node_id,
        #                 "y":node_id},
        # # and edges between nodes
        # data["edges"] += {"id":"e{0}".format(node_id),
        #                 "source":"n0",
        #                 "target":"n{0}".format(node_id)},

        all_links.append(links)


    # return json.dumps(all_links)
    return all_links
    # with open('sigma/data/test.json', 'w') as outfile:
    #     json.dump(data, outfile, indent=2)




if __name__ == '__main__':
    get_page_links("Scotland")
