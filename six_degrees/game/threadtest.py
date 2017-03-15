import threading
import time
from Queue import Queue

def add_node(link):
    time.sleep(1)
    print "added node " + link
    return

def add_edge(link):
    # needs to be done after add_node
    print "added edge to " + link
    return

def process(queue, link):
    for i in range(0, queue.qsize()):
        func = queue.get()
        func(link)

def new_queue():
    q = Queue()
    q.put(lambda x: add_node(x))
    q.put(lambda x: add_edge(x))
    return q

links = ["england", "scotland", "ireland", "wales"]
threads = []
for link in links:
    q = new_queue()
    t = threading.Thread(target=process, args=(q,link,))
    threads.append(t)
    t.start()

[thread.join() for thread in threads]
print "done"

def thread_add(current_node):
    start_time = time.time()
    all_links = get_links_for(current_node["name"])
    if all_links is None:
        return None

    # avoids stupid quotations breaking queries
    all_links = [link for link in all_links if not contains_quotes(link["title"])]

    # converts the links into nodes format
    threads = []
    for link in all_links:
        q = Queue()

        link["name"] = link.pop("title")
        link.pop("ns")

        if not node_exists(link):
            print 'node does not exist '
            q.put(lambda x: add_node(x))

        # otherwise always add relationship
        q.put(lambda x,y,z: add_edge(x, y, z))

        t = threading.Thread(target=process, args=(q, link, current_node,))
        threads.append(t)
        t.start()

    [thread.join() for thread in threads]
    print "--- %s seconds ---" % (time.time() - start_time)
    return True


def process(queue, link, current_node):
    for i in range(0, queue.qsize()):
        try:
            func = queue.get()
            func(link)
        except:
            func = queue.get()
            func(current_node, link, "linksTo")
