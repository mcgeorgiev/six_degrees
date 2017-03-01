from neo4j.v1 import GraphDatabase, basic_auth

def get_session():
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "password"))
    return driver.session()


def get_nodes_from_game(start, game, end):
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "password"))
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


def add_node(article, wiki_id):
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "password"))
    session = driver.session()
    # need to escape the curly braces
    query = "CREATE ({0}:Article {{name:'{1}', id:{2}}})".format(format_string(article), article, wiki_id)
    print query
    session.run(query)
    session.close()


def create_session():
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "password"))
    session =  driver.session()
    print session
    return session


def add_edge(nodeA, nodeB, game_id):
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "password"))
    session =  driver.session()

    query = """MATCH (a:Article),(b:Article) WHERE a.name = '{0}' AND b.name = '{1}'
               CREATE (a)-[r:{2}]->(b)""".format(nodeA["name"], nodeB["name"], game_id)
    session.run(query)
    session.close()


def get_node_from_name(name):
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "password"))
    session =  driver.session()

    query = "match (node:Article{{name: '{0}'}}) return node".format(name)
    results = session.run(query)
    session.close()
    for record in results:
        return record['node'].properties


def get_related_nodes(node):
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "password"))
    session =  driver.session()

    query = "MATCH (Article {{ name: '{0}' }})--(related) return related".format(node["name"])
    results = session.run(query)
    session.close()

    all_nodes = []
    for record in results:
        all_nodes.append(record["related"].properties)
    distinct_nodes = {value['id']:value for value in all_nodes}.values()
    return distinct_nodes


def has_enough_edges(current_node):
    # if the node has one relationship then that is it's source
    min_relations = 10
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "password"))
    session =  driver.session()

    query = "MATCH (Article {{ name: '{0}' }})--(related) return related.name".format(current_node["name"])
    results = session.run(query)
    session.close()

    all_relations = []
    for record in results:
        all_relations.append(record["related.name"])
    distinct_relations = frozenset(all_relations)

    return True if len(distinct_relations) >= min_relations else False

def player_selects_node():
    current = {}
    if has_enough_edges(current_node):
        get_related_nodes(current_node)
        # return the nodes to the front end
    else:
        pass

def does_not_exist():
    # make sure duplicates are not added
    pass

def add_API_nodes():
    pass

def format_string(string):
    string = string.replace(" ", "_")
    string = string.lower()
    return string



# * Useful code to find an objects properties names
# for property, value in vars(related).iteritems():
#     print property, ": ", value

if __name__ == "__main__":
    print get_related_nodes(get_node_from_name("Neolithic"))
    #print has_enough_edges({"name": "Neolithic"})
    #add_edge({"name": "England"}, {"name": "Scotland"}, "game3")
    #add_node("England", 9)
    #add_node("Anglican Communion", 8)

    # start = "scotland"
    # game = "game2"
    # end = "kangaroo"
    #
    # get_nodes_from_game(start, game, end)
