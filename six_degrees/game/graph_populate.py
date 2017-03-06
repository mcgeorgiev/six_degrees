from graph import execute




def wipe_database():
    query = "MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r"
    execute(query)
    print "Wiping database..."

def create_nodes():
    query = """
        create (:Article {name:"Scotland"})
        create (:Article {name:"William Wallace"})
        create (:Article {name:"Rob Roy"})
        create (:Article {name:"Glasgow"})
        create (:Article {name:"England"})
        create (:Article {name:"Thistle"})
        create (:Article {name:"Scottish Parliament"})
        create (:Article {name:"Isle of Arran"})
    """
    execute(query)
    print "Creating new nodes..."

def create_relationships():
    queries = [
        """
        MATCH (a:Article),(b:Article) WHERE a.name = 'Scotland' AND b.name = 'William Wallace'
        CREATE (a)-[r:linksTo]->(b)""",
        """
        MATCH (a:Article),(b:Article) WHERE a.name = 'Scotland' AND b.name = 'Rob Roy'
        CREATE (a)-[r:linksTo]->(b)""",
        """
        MATCH (a:Article),(b:Article) WHERE a.name = 'Scotland' AND b.name = 'Glasgow'
        CREATE (a)-[r:linksTo]->(b)""",
        """
        MATCH (a:Article),(b:Article) WHERE a.name = 'Scotland' AND b.name = 'England'
        CREATE (a)-[r:linksTo]->(b)""",
        """
        MATCH (a:Article),(b:Article) WHERE a.name = 'Scotland' AND b.name = 'Thistle'
        CREATE (a)-[r:linksTo]->(b)""",
        """
        MATCH (a:Article),(b:Article) WHERE a.name = 'Scotland' AND b.name = 'Scottish Parliament'
        CREATE (a)-[r:linksTo]->(b)""",
        """
        MATCH (a:Article),(b:Article) WHERE a.name = 'Scotland' AND b.name = 'Isle of Arran'
        CREATE (a)-[r:linksTo]->(b)"""
        ]

    for query in queries:
        execute(query)
    print "Creating relationships between nodes"


if __name__ == "__main__":
    wipe_database()
    create_nodes()
    create_relationships()
