from neo4j.v1 import GraphDatabase, basic_auth
from Wiki import get_page_links
import random
from itertools import count


def get_nodes_from_game(start, game, end):
    driver = driver_connection()
    session = driver.session()

    query = "match ({0})-[l:{1}]->({2}) return {0}, type(l), {2}".format(start, game, end)
    result = session.run(query)

    output = {"game": game,
              "nodes": []}

    for record in result:
        entry = {  "source" : {
                    "name": record[start].properties['name'],
                    "id": record[start].properties['id']
                },
                    "dest" : {
                    "name": record[end].properties['name'],
                    "id": record[end].properties['id']
                }
        }

        # if the list is empty add the entry
        if len(output["nodes"]) == 0:
            output["nodes"].append(entry)
        else:
            # if the list is not empty determine whether to insert before or after the relevant entries
            for i in range(len(output["nodes"])):
                if entry["dest"]["name"] == output["nodes"][i]["source"]["name"]:
                    output["nodes"].insert(i, entry)
                    break
                elif entry["source"]["name"] == output["nodes"][i]["dest"]["name"]:
                    output["nodes"].insert(i+1, entry)
                    break
    session.close()
    print output
    return output


def add_node(node):
    driver = driver_connection()
    session = driver.session()
    # need to escape the curly braces
    try:
        query = "CREATE (node:Article {{name:'{0}', id:{1}}})".format(node["name"], node["id"])
        print query
        session.run(query)
        session.close()
    except:
        print "Unicode is not added."



def add_edge(nodeA, nodeB, relationship_name):
    driver = driver_connection()
    session = driver.session()

    query = """MATCH (a:Article),(b:Article) WHERE a.name = '{0}' AND b.name = '{1}'
               CREATE (a)-[r:{2}]->(b)""".format(nodeA["name"], nodeB["name"], relationship_name)
    session.run(query)
    session.close()


def get_node_from_name(name):
    driver = driver_connection()
    session = driver.session()

    query = "match (node:Article{{name: '{0}'}}) return node".format(name)
    results = session.run(query)
    session.close()
    for record in results:
        return record['node'].properties


def get_related_nodes(node):
    driver = driver_connection()
    session = driver.session()

    query = "MATCH (Article {{ name: '{0}' }})--(related) return related".format(node["name"])
    results = session.run(query)
    session.close()

    all_nodes = []
    for record in results:
        print record
        all_nodes.append(record["related"].properties)
    distinct_nodes = {value['name']:value for value in all_nodes}.values()

    return distinct_nodes


def has_enough_edges(current_node):
    # if the node has one relationship then that is it's source
    min_relations = 5
    driver = driver_connection()
    session = driver.session()

    query = "MATCH (Article {{ name: '{0}' }})--(related) return related.name".format(current_node["name"])
    results = session.run(query)
    session.close()

    all_relations = []
    for record in results:
        all_relations.append(record["related.name"])
    distinct_relations = frozenset(all_relations)

    return True if len(distinct_relations) >= min_relations else False





def driver_connection():
    #return GraphDatabase.driver("bolt://hobby-nlhlodhmoeaggbkehnjmnbol.dbs.graphenedb.com:24786", auth=basic_auth("testing", "b.g3C3SxcDglNv.anE0GtQ64r8M7WkS"))

    return GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "password"))


def node_exists(node):
    # make sure duplicates are not added
    driver = driver_connection()
    session = driver.session()
    try:
        query = "MATCH (Article {{ name: '{0}' }}) return Article".format(node["name"])
        results = session.run(query)
        session.close()
        return True if results.peek() is not None else False
    except:
        return False



def add_API_nodes(current_node):
    all_links = get_page_links(current_node["name"])
    if all_links is None:
        return None
    # avoids stupid quotations breaking queries
    all_links = [link for link in all_links if not contains_quotes(link["title"])]
    # converts the links into nodes format
    for link in all_links:
        link["id"] = link.pop("ns")
        link["id"] = random.randint(0, 10000) # just for testing
        link["name"] = link.pop("title")
    print all_links
    for link in all_links:
        if not node_exists(link):
            print 'here'
            add_node(link)
        # otherwise always add relationship
        add_edge(current_node, link, "linksTo")
    return True


def contains_quotes(name):
    return True if "'" in name or '"' in name else False


def format_string(string):
    string = string.replace(" ", "_")
    string = string.lower()
    return string



# * Useful code to find an objects properties names
# for property, value in vars(related).iteritems():
#     print property, ": ", value

if __name__ == "__main__":
    print get_related_nodes({"name": "Neolithic"})
    #add_API_nodes(get_node_from_name("Kangaroo"))
    #print has_enough_edges({"name": "Neolithic"})
    #add_edge({"name": "England"}, {"name": "Scotland"}, "game3")
    #add_node("England", 9)
    #add_node("Anglican Communion", 8)

    # start = "scotland"
    # game = "game2"
    # end = "kangaroo"
    #
    # get_nodes_from_game(start, game, end)
