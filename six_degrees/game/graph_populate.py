from graph import connection

def wipe_database():
    gdb = connection()
    query = "MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r"
    gdb.query(query)
    print "Wiping database..."

def create_start_node():
    gdb = connection()
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
    gdb.query(query)
    print "Creating new nodes..."

def create_end_node():
    gdb = connection()
    query = """
        create (:Article {name:"Australia"})
        create (:Article {name:"Kangaroo"})
        create (:Article {name:"Crocodile Dundee"})
        create (:Article {name:"Mates"})
        create (:Article {name:"Bondi Beach"})
        create (:Article {name:"Bogan"})
    """
    gdb.query(query)
    print "Creating end node"

def create_end_relationships():
    gdb = connection()
    queries = [
        """
        MATCH (a:Article),(b:Article) WHERE a.name = 'Australia' AND b.name = 'Kangaroo'
        CREATE (a)-[r:linksTo]->(b)""",
        """
        MATCH (a:Article),(b:Article) WHERE a.name = 'Australia' AND b.name = 'Crocodile Dundee'
        CREATE (a)-[r:linksTo]->(b)""",
        """
        MATCH (a:Article),(b:Article) WHERE a.name = 'Australia' AND b.name = 'Mates'
        CREATE (a)-[r:linksTo]->(b)""",
        """
        MATCH (a:Article),(b:Article) WHERE a.name = 'Australia' AND b.name = 'Bondi Beach'
        CREATE (a)-[r:linksTo]->(b)""",
        """
        MATCH (a:Article),(b:Article) WHERE a.name = 'Australia' AND b.name = 'Bogan'
        CREATE (a)-[r:linksTo]->(b)"""
        ]

    for query in queries:
        gdb.query(query)
    print "Creating end relationships between nodes"


def create_relationships():
    gdb = connection()
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
        gdb.query(query)
    print "Creating relationships between nodes"


if __name__ == "__main__":
    wipe_database()
    create_start_node()
    create_end_node()
    create_relationships()
    create_end_relationships()
