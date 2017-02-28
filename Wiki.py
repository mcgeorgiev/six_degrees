import requests
import json
from itertools import count

# page id to get links currently all links from "broughty ferry" page
def get_page_links(name):
    page_name = name

    api_url = "https://en.wikipedia.org/w/api.php?action=query&titles={0}&prop=links&pllimit=10&format=json".format(page_name)

    r = requests.get(api_url)
    resp = r.json()

    #page_id = resp['query']['pages']['360393']['pageid']
    for nested_json in resp["query"]["pages"]:
        page_id = nested_json
    print page_id
    # build json response with all current nodes
    data = {}
    data["nodes"] = [{"id":"n0", "label":resp["query"]["pages"]["{0}".format(page_id)]["title"], "x":0, "y":0, "size":2}]
    data["edges"] = []
    counter = count(1)
    for links in resp["query"]["pages"]["{0}".format(page_id)]["links"]:
        # print links['title']
        node_id = counter.next()
        data["nodes"] += {"id":"n{0}".format(node_id),
                        "label":links['title'],
                        "size":1,
                        "x":node_id,
                        "y":node_id},
        data["edges"] += {"id":"e{0}".format(node_id),
                        "source":"n{0}".format((node_id-1)),
                        "target":"n{0}".format(node_id)},

    with open('sigma/data/test.json', 'w') as outfile:
        json.dump(data, outfile, indent=2)
if __name__ == '__main__':
    get_page_links("Broughty Ferry")
