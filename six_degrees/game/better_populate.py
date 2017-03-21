from wiki_scraper import get_shortest_path
import threading
import time
from graph import *

def wipe_database():
    gdb = connection()
    query = "MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r"
    gdb.query(query)
    print "Wiping database..."


sources = ["Scotland", "England"]#, "Pizza", "SQL"]
destinations = ["Haskell", "Kangaroo"]#, "Kevin Bacon", "Java"]

def create_pairs(sources, destinations):
    # pairs between the sources
    pair_list = []
    for source in sources:
        for dest in destinations:
            pair = [source, dest]
            pair_list.append(pair)
    return pair_list

def worker(pair):
    all_paths.append(get_shortest_path(pair[0], pair[1]))

global all_paths
all_paths = []

pairs = create_pairs(sources, destinations)
threads = []
for pair in pairs:
    t = threading.Thread(target=worker, args=(pair, ))
    threads.append(t)
    t.start()

[thread.join() for thread in threads]
print "done"

#wipe_database()
