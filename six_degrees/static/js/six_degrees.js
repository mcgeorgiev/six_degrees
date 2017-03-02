// Add a method to the graph model that returns an
// object with every neighbors of a node inside:

var data = {
  "nodes": [
    {
      "id": "n0",
      "label": "scotland",
      "x": 0,
      "y": 0,
      "size": 3
  }]}


sigma.classes.graph.addMethod('neighbors', function(nodeId) {
  var k,
      neighbors = {},
      index = this.allNeighborsIndex[nodeId] || {};

  for (k in index)
    neighbors[k] = this.nodesIndex[k];

  return neighbors;
});

sigma.parsers.json(
    {data,
  {
    container: 'container',
    settings: {
      labelThreshold : 0
    }
  },
  function(s) {
    // We first need to save the original colors of our
    // nodes and edges, like this:
    s.graph.nodes().forEach(function(n) {
      n.originalColor = n.color;
    });
    s.graph.edges().forEach(function(e) {
      e.originalColor = e.color;
    });

    // When a node is clicked, we check for each node
    // if it is a neighbor of the clicked one. If not,
    // we set its color as grey, and else, it takes its
    // original color.
    // We do the same for the edges, and we only keep
    // edges that have both extremities colored.
    s.bind('clickNode', function(e) {
      //alert(e.data.node.label);
      var nodeId = e.data.node.id,
          toKeep = s.graph.neighbors(nodeId);
      toKeep[nodeId] = e.data.node;

      if (e.data.node.id == 'n0') {
          s.graph.addNode({ id: 'n5',
            "x": 1,
            "y": 2,
            "size": 1 });
          s.graph.addEdge({
            id: 'e5',
            source: 'n5',
            target: 'n0'
          });
          s.refresh();
      }
      // s.graph.addNode({ id: 'n5',
      //       "x": 1,
      //       "y": 2,
      //       "size": 1 });
      // s.graph.addEdge({
      //   id: 'e5',
      //   source: 'n5',
      //   target: 'n0'
      // });
      // s.refresh();
      // Since the data has been modified, we need to
      // call the refresh method to make the colors
      // update effective.
      //s.refresh();
    });
  }
);
