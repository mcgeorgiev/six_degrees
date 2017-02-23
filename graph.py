from neo4j.v1 import GraphDatabase, basic_auth

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
    print output
    return output

if __name__ == "__main__":
    start = "scotland"
    game = "game2"
    end = "kangaroo"

    get_nodes_from_game(start, game, end)
