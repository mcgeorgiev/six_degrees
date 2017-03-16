from neo4j.v1 import GraphDatabase, basic_auth
from Wiki import get_links_for
import random
from itertools import count
from neo4jrestclient.client import GraphDatabase

def connection():
    return GraphDatabase("http://localhost:7474/db/data/", username="neo4j", password="password")
    #return GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "password"))
    #return GraphDatabase("http://hobby-ekngppohojekgbkepjibeaol.dbs.graphenedb.com:24789/db/data/", username="testing-user", password = "b.SIxCtcPc51R5.aaW8WZa65LdsjGgZ")


# def get_nodes_from_game(start, game, end):
#     driver = driver_connection()
#     session = driver.session()
#
#     query = "match ({0})-[l:{1}]->({2}) return {0}, type(l), {2}".format(start, game, end)
#     result = session.run(query)
#
#     output = {"game": game,
#               "nodes": []}
#
#     for record in result:
#         entry = {  "source" : {
#                     "name": record[start].properties['name'],
#                     "id": record[start].properties['id']
#                 },
#                     "dest" : {
#                     "name": record[end].properties['name'],
#                     "id": record[end].properties['id']
#                 }
#         }
#
#         # if the list is empty add the entry
#         if len(output["nodes"]) == 0:
#             output["nodes"].append(entry)
#         else:
#             # if the list is not empty determine whether to insert before or after the relevant entries
#             for i in range(len(output["nodes"])):
#                 if entry["dest"]["name"] == output["nodes"][i]["source"]["name"]:
#                     output["nodes"].insert(i, entry)
#                     break
#                 elif entry["source"]["name"] == output["nodes"][i]["dest"]["name"]:
#                     output["nodes"].insert(i+1, entry)
#                     break
#     session.close()
#     print output
#     return output
#
#
def add_node(node):
    gdb = connection()
    # need to escape the curly braces
    try:
        query = "CREATE (node:Article {{name:'{0}'}})".format(node["name"])
        print query
        gdb.query(query)
    except:
        print "Unicode is not added."


def add_edge(nodeA, nodeB, relationship_name):
    gdb = connection()

    try:
        query = """MATCH (a:Article),(b:Article) WHERE a.name = '{0}' AND b.name = '{1}'
                   CREATE (a)-[r:{2}]->(b)""".format(nodeA["name"], nodeB["name"], relationship_name)
        gdb.query(query)
    except:
        print "Unicode is not added"


def get_node_from_name(name):
    gdb = connection()

    query = "match (node:Article{{name: '{0}'}}) return node".format(name)
    results = gdb.query(query)
    for record in results:
        return record[0]['data']


def get_related_nodes(node):
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

    try:
        output_dict["related"].remove(starting_node)
    except ValueError:
        print "All good removing starting node from related node list"

    return output_dict


def get_end_node(starting_name, related_names):
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
    # make sure duplicates are not added
    gdb = connection()
    query = "MATCH (Article {{ name: '{0}' }}) return Article".format(node["name"].encode('utf-8'))
    results = gdb.query(query)
    try:
        existing_node = results[0]
        return True
    except IndexError:
        return False


def add_API_nodes(current_node, end_name):
    all_links = get_links_for(current_node["name"], end_name)
    if all_links is None:
        return None

    # avoids stupid quotations breaking queries
    all_links = [link for link in all_links if not contains_quotes(link["title"])]

    # converts the links into nodes format
    for link in all_links:
        link["name"] = link.pop("title")
        link.pop("ns")

        if not node_exists(link):
            print 'node does not exist - added'
            add_node(link)

        # otherwise always add relationship
        add_edge(current_node, link, "linksTo")
    return True


def contains_quotes(name):
    return True if "'" in name or '"' in name else False


def add_game_relationship(nodes, game_id):
    query_string = ""
    gdb = connection()
    print type(nodes)
    print nodes[0]
    print "----"
    for i in range(1,len(nodes)):
        source = nodes[i-1]["label"]
        dest = nodes[i]["label"]
        query = "MATCH (a:Article {{name:'{0}'}}), (b:Article {{name:'{1}'}}) CREATE (a)-[:game{2}]->(b)".format(source, dest, game_id)
        gdb.query(query)

def get_id():
    gdb = connection()
    query = "match (m:Article {name: 'Australia'})-[r:linksTo]-(p:Article {name: 'Bondi Beach'}) return r"
    results = gdb.query(query)
    for r in results:
        print r


def get_shortest_path(source, dest):
    query = """
    MATCH p=shortestPath(
    (a:Article {{name:"{0}"}})-[*]-(b:Article {{name:"{1}"}}))
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
            node_id_list.append(node.split("/")[-1])
        break
    return get_names_from_ids(node_id_list)


def get_names_from_ids(id_list):
    id_list =  str([int(i) for i in id_list])

    query = """
    MATCH (a:Article)
    WHERE id(a) IN {}
    RETURN a.name
    """.format(id_list)

    gdb = connection()
    results = gdb.query(query)
    return [name[0] for name in results]


# * Useful code to find an objects properties names
# for property, value in vars(related).iteritems():
#     print property, ": ", value

if __name__ == "__main__":
    #print get_shortest_path("Victoria (Australia)", "Sydney")
    nodes = [
      {
        "id": 101,
        "label": "Sydney"
      },
      {
        "id": 67,
        "label": "Crocodile Dundee"
      },
      {
        "id": 65,
        "label": "Australia"
      },
      {
        "id": 69,
        "label": "Bondi Beach"
      }
    ]
    #add_game_relationship(nodes)
    # print node_exists(node)
    # print nodes_with_num_relations(4)
    print get_related_nodes({"name": "Glasgow"})
    # add_API_nodes(get_node_from_name("Kangaroo"))
    # print get_node_from_name("Australia")
    # print get_end_node("Scotland", ["Isle of Arran", "Scottish Parliament", "Thistle", "England", "Glasgow", "Rob Roy", "William Wallace"])
    # print has_enough_edges({"name": "Glasgow"})
    #add_edge({"name": "England"}, {"name": "Scotland"}, "game3")
    #add_node("England", 9)
    #add_node("Anglican Communion", 8)

    # start = "scotland"
    # game = "game2"
    # end = "kangaroo"
    #
    # get_nodes_from_game(start, game, end)
