import requests

# page id to get links currently all links from "broughty ferry" page
page_id = 360393

api_url = "https://en.wikipedia.org/w/api.php?action=query&pageids=%s&prop=links&pllimit=max&format=json" % page_id

r = requests.get(api_url)
resp = r.json()

for links in resp['query']['pages']['%d'%page_id]['links']:
    print links['title']
