from Wiki import get_links_for
from neo4jrestclient.client import GraphDatabase
from Queue import Queue
import threading
import time

def connection():
    """Return a connection object."""
    return GraphDatabase("http://localhost:7474/db/data/", username="neo4j", password="password")
    #return GraphDatabase("http://hobby-pmaccehmoeaggbkehkbfidol.dbs.graphenedb.com:24789/db/data/", username="admin-user", password = "b.JByrrlXaTWie.4ljs0uLwKIhUl21h")


def add_node(node):
    """Add a given node to the database"""
    gdb = connection()
    try:
        query = "CREATE (node:Article {{name:'{0}'}})".format(node["name"])
        print query
        gdb.query(query)
    except:
        print "Unicode is not added."


def add_edge(nodeA, nodeB, relationship_name):
    """Add a given relationship between two nodes"""
    gdb = connection()

    try:
        query = """MATCH (a:Article),(b:Article) WHERE a.name = '{0}' AND b.name = '{1}'
                   CREATE (a)-[r:{2}]->(b)""".format(nodeA["name"], nodeB["name"], relationship_name)
        gdb.query(query)
        print "added edge"
    except:
        print "Unicode is not added"


def get_node_from_name(name):
    """Return a node by its name"""
    gdb = connection()

    query = "match (node:Article{{name: '{0}'}}) return node".format(name)
    results = gdb.query(query)
    for record in results:
        return record[0]['data']


def get_related_nodes(node):
    """Returns a list of distinct related nodes for a node."""

    gdb = connection()
    query = "MATCH (Article {{ name: '{0}' }})--(related) return related".format(node["name"])
    results = gdb.query(query)
    all_nodes = []
    for record in results:
        related_node = {}
        related_node["id"] = record[0]["metadata"]["id"]
        related_node["name"] = record[0]['data']["name"]
        all_nodes.append(related_node)
    distinct_nodes = {value['name']:value for value in all_nodes}.values()
    return distinct_nodes


def has_enough_edges(current_node):
    """Returns True if the current node has 5 or more distinct relations"""

    # if the node has one relationship then that is it's source
    min_relations = 5
    gdb = connection()

    query = "MATCH (Article {{ name: '{0}' }})--(related) return related.name".format(current_node["name"])
    results = gdb.query(query)

    all_relations = []
    for record in results:
        all_relations.append(record[0])
    distinct_relations = frozenset(all_relations)
    print "Number of relations: " + str(len(distinct_relations))

    return True if len(distinct_relations) >= min_relations else False


def nodes_with_num_relations(min_number):
    """Returns a random starting node and it's relations and a random end node"""

    gdb = connection()
    query = """
            MATCH (start)-[]->(b)
            WITH start, count(b) as relations, collect(b) as relatednodes
            WHERE relations > {}
            RETURN start, relatednodes, relations, rand() as r
            ORDER BY r
            """.format(min_number)

    results = gdb.query(query)[0]
    # first element of returned list is the start node
    start = results.pop(0)
    starting_node = {}
    starting_node["name"] = start['data']["name"]
    starting_node["id"] = start["metadata"]["id"]

    # next element are the related nodes
    relatednodes = results[0]
    related_nodes_list = []
    for node in relatednodes:
        related = {}
        related["name"] = node['data']["name"]
        related["id"] = node["metadata"]["id"]
        related_nodes_list.append(related)

    # get the end node, so it is not the start or related
    end_node = get_end_node(starting_node["name"], [node["name"] for node in related_nodes_list])

    output_dict = {}
    output_dict["start"] = starting_node
    output_dict["related"] = {value['name']:value for value in related_nodes_list}.values()
    output_dict["end"] = end_node

    # try to remove the starting node if contained in related
    try:
        output_dict["related"].remove(starting_node)
    except ValueError:
        print "All good removing starting node from related node list"

    # makes sure the there is a connection between the start and end nodes
    path = get_shortest_path(output_dict['start']["name"], output_dict['end']["name"])
    if len(path) == 0:
        print "Searching again"
        return nodes_with_num_relations(min_number)
    else:
        return output_dict


def get_start_data():
    """Gets the starting nodes with a min number of relations."""
    return nodes_with_num_relations(4)


def get_end_node(starting_name, related_names):
    """ Recursive function to get a random end node which is not the same as
        the starting node or is already in the starting relations."""

    gdb = connection()
    query = """
            MATCH (end)-[]->(b)
            RETURN end, rand() as r
            ORDER BY r
            """
    results = gdb.query(query)

    end_node = {}
    end_node["id"] = results[0][0]["metadata"]["id"]
    end_node["name"] = results[0][0]['data']["name"]

    if end_node["name"] == starting_name or end_node["name"] in related_names:
        return get_end_node(starting_name, related_names)
    else:
        return end_node


def node_exists(node):
    """Checks to see if a node has been added to the database already."""
    # make sure duplicates are not added
    gdb = connection()
    query = "MATCH (Article {{ name: '{0}' }}) return Article".format(node["name"].encode('utf-8'))
    results = gdb.query(query)
    try:
        existing_node = results[0]
        return True
    except IndexError:
        return False


def process(queue, current_node, link):
    """The thread process to execute lambda functions"""
    length = queue.qsize()
    for i in range(0, length):
        print i
        func = queue.get()
        try:
            func(link)
        except TypeError:
            func(current_node, link, "linksTo")


def add_API_nodes(current_node, end_name):
    """ Queries the API for a list of related nodes from the current_node and
        their relationships to be added to the database.
        The process is multithreaded."""
    #add_node(current_node["name"])

    start_time = time.time()
    all_links = get_links_for(current_node["name"], end_name)
    if all_links is None:
        return None
    # avoids stupid quotations breaking queries
    all_links = [link for link in all_links if not contains_quotes(link["title"])]

    threads = []
    for link in all_links:
        print link
        q = Queue()

        link["name"] = link.pop("title")
        link.pop("ns")

        # adds anonymous functions to a queue to be executed in the thread process
        if not node_exists(link):
            print 'node does not exist '
            add = lambda x: add_node(x)
            q.put(add)

        # otherwise always add relationship
        edge = lambda x,y,z: add_edge(x, y, z)
        q.put(edge)

        t = threading.Thread(target=process, args=(q, current_node, link))
        threads.append(t)
        t.start()

    [thread.join() for thread in threads]
    print "--- adding nodes took %s seconds ---" % (time.time() - start_time)
    return True


def contains_quotes(name):
    """Returns true if string contains quotations"""
    return True if "'" in name or '"' in name else False


def add_game_relationship(nodes, game_id):
    """Add a relationship for a list of nodes with a user's game id"""
    gdb = connection()
    for i in range(1,len(nodes)):
        source = nodes[i-1]["label"]
        dest = nodes[i]["label"]
        query = "MATCH (a:Article {{name:'{0}'}}), (b:Article {{name:'{1}'}}) CREATE (a)-[:game{2}]->(b)".format(source, dest, game_id)
        gdb.query(query)


def get_shortest_path(source, dest):
    """Returns the ids of a shortest path between a source and a destination."""

    query = """
    MATCH p=shortestPath(
    (a:Article {{name:"{0}"}})-[*]->(b:Article {{name:"{1}"}}))
    RETURN p
    ORDER BY LENGTH(p) ASC
    LIMIT 1
    """.format(source, dest)

    gdb = connection()
    results = gdb.query(query)

    node_id_list = []
    for result in results:
        node_url = result[0]["nodes"]
        for node in node_url:
            # extract the last part of the url which is the node id
            node_id_list.append(node.split("/")[-1])
        break
    return get_names_from_ids(node_id_list)


def get_names_from_ids(id_list):
    """ Returns a list of the names of Articles from a list of node ids"""

    id_list =  str([int(i) for i in id_list])
    query = """
    MATCH (a:Article)
    WHERE id(a) IN {}
    RETURN a.name
    """.format(id_list)

    gdb = connection()
    results = gdb.query(query)
    return [name[0] for name in results]


if __name__ == "__main__":
    """Old tests for graph.py """
    pass

    # does_connection_exist("Australia", "Crocodile Dundee")
    # print get_shortest_path("Bondi Beach", "Crocodile Dundee")
    # add_game_relationship(nodes)
    # print node_exists(node)
    # nodes_with_num_relations(4)
    # print get_related_nodes({"name": "Glasgow"})
    # add_API_nodes(get_node_from_name("Kangaroo"))
    # print get_node_from_name("Australia")
    # print get_end_node("Scotland", ["Isle of Arran", "Scottish Parliament", "Thistle", "England", "Glasgow", "Rob Roy", "William Wallace"])
    # print has_enough_edges({"name": "Glasgow"})
    # add_edge({"name": "England"}, {"name": "Scotland"}, "game3")
    # add_node("England", 9)
    # add_node("Anglican Communion", 8)
