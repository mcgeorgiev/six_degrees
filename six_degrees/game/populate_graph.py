from graph import connection
import csv
import requests
import time
import threading
from graph import add_node, add_edge, contains_quotes, node_exists
from Queue import Queue

#"""CREATE INDEX ON :Article(name);"""

def wipe_database():
    gdb = connection()
    query = "MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r"
    gdb.query(query)
    print "Wiping database..."


def add_csv_nodes():
    with open("small_data.csv", "r") as input:
        for name in csv.reader(input):
            add_API_nodes(name[0])

def add_API_nodes(name):
    add_node(name)

    start_time = time.time()
    all_links = get_top_links(name)
    #print all_links
    if all_links is None:
        return None
    #print len(all_links)
    # avoids stupid quotations breaking queries
    all_links = [link for link in all_links if not contains_quotes(link["title"])]

    threads = []
    for link in all_links:
        print link
        q = Queue()
        print link
        try:
            link["name"] = link.pop("title")
            link.pop("ns")
        except:
            pass

        if not node_exists(link):
            print 'node does not exist '
            add = lambda x: add_node(x)
            q.put(add)

        # otherwise always add relationship
        edge = lambda x,y,z: add_edge(x, y, z)
        q.put(edge)

        t = threading.Thread(target=process, args=(q, name, link))
        threads.append(t)
        t.start()

    [thread.join() for thread in threads]
    print "--- adding nodes took %s seconds ---" % (time.time() - start_time)
    return True


def process(queue, current_node, link):
    length = queue.qsize()
    for i in range(0, length):
        print i
        func = queue.get()
        try:
            func(link)
        except TypeError:
            func(current_node, link, "linksTo")


def get_top_links(name):
    global all_links
    all_links = []
    get_page(name)
    filtered_links = remove_meta_links(all_links)
    if filtered_links == []:
        return None

    chosen_links = []
    for i in range(0, len(filtered_links)-1):
        file_data = open('small_data.csv', 'r')

        csv_data = csv.reader(file_data)
        for item in csv_data:
            if filtered_links[i]["title"] == unicode(item[0]):
                chosen_links.append(filtered_links[i])


    file_data.close()

    for i in range(len(filtered_links)):
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

if __name__ == "__main__":
    wipe_database()
    add_csv_nodes()
