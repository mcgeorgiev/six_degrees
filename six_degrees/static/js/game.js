///////////////// DATA DEFINITION FOR TESTING /////////////////////
var data = {
  "nodes": [
    {
      "y": 0,
      "x": 0,
      "size": 3,
      "id": "n0",
      "label": "Dundee"
    },
    {
      "y": 1,
      "x": 1,
      "size": 1,
      "id": "n1",
      "label": "1906 Dundee fire"
    },
    {
      "y": -1,
      "x": -1,
      "size": 1,
      "id": "n2",
      "label": "4J Studios"
    },
    {
      "y": 0,
      "x": 1,
      "size": 1,
      "id": "n3",
      "label": "5th Scottish Parliament"
    },
    {
      "y": 1,
      "x": 0,
      "size": 1,
      "id": "n4",
      "label": "A.C. Milan"
    },
    {
      "y": -1,
      "x": 0,
      "size": 1,
      "id": "n5",
      "label": "A.S. Roma"
    }
  ],
  "edges": [
    {
      "source": "n0",
      "id": "e1",
      "target": "n1"
    },
    {
      "source": "n0",
      "id": "e2",
      "target": "n2"
    },
    {
      "source": "n0",
      "id": "e3",
      "target": "n3"
    },
    {
      "source": "n0",
      "id": "e4",
      "target": "n4"
    },
    {
      "source": "n0",
      "id": "e5",
      "target": "n5"
    }
  ]
}

/////////////////////// START SIGMA STUFF ///////////////////////////


  sigma.classes.graph.addMethod('neighbors', function(nodeId) {
  var k,
      neighbors = {},
      index = this.allNeighborsIndex[nodeId] || {};

  for (k in index)
    neighbors[k] = this.nodesIndex[k];

  return neighbors;
  });

  // Let's first initialize sigma:
  s = new sigma({
      graph: data,
      container: 'container',
      settings: {
          defaultNodeColor: '#666',
          labelThreshold: 0
      }
  });

  var currentNode=null;

  // user has clicked a node
  s.bind('clickNode', function(e) {

    var nodeId = e.data.node.id;
    toKeep = s.graph.neighbors(nodeId);
    toKeep[nodeId] = e.data.node;
    var newNode = Math.random();
    if (e.data.node.id == currentNode || currentNode == null) {
      // make the previous node and edge green to differentiate path
      e.data.node.color = '#696';
      e.data.node.size = 3;

      var next_node = e.data.node.label;
      console.log(next_node);

      s.graph.edges().forEach(function(e) {
          if(e.source == currentNode) {
              e.color = '#696';
      }});

      // add the new "main" node
      s.graph.addNode({ id: newNode,
        "x": e.data.node.x + Math.random(),
        "y": e.data.node.x + Math.random(),
        "size": 5,
        "color": "#f00"});
      s.graph.addEdge({
        id: newNode,
        source: newNode,
        target: e.data.node.id,
      });
      var n = s.graph.nodes(newNode);

      // move camera to look at the new node
      sigma.misc.animation.camera(
        s.camera,
        {
          x: n[s.camera.readPrefix + 'x'],
          y: n[s.camera.readPrefix + 'y'],
          ratio: 1
        },
        { duration: s.settings('animationsTime') }
      );
      s.refresh();
      currentNode = newNode;

      var url_get = "http://127.0.0.1:8000/game/incomingnode/"+next_node;
      console.log(url_get);
      // use ajax to get the next set of nodes branching from this main node
      next_nodes(url_get, callback);
  }});

  // Finally, update sigma
  s.refresh();

//////////////////// FUNCTIONS ///////////////////
function next_nodes(url_get, callback) {
  $.ajax({
      url: url_get,
      datatype: 'json',
      success: function(data) {
          callback(data);
      },
      failure: function(data) {
          alert('Something went wrong! Please try again.');
      }
    });
  }
  function callback(data) {
    var json = JSON.parse(data);
    jQuery.each(json, function(i, val) {
      alert(val["title"]);
    });
  }
