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

new sigma.classes.configurable(
  {
    autoRescale: false,
    autoResize: false,
  });

  sigma.classes.graph.addMethod('neighbors', function(nodeId) {
  var k,
      neighbors = {},
      index = this.allNeighborsIndex[nodeId] || {};

  for (k in index)
    neighbors[k] = this.nodesIndex[k];

  return neighbors;
  });

  // Let's first initialize sigma:
  var s = new sigma({
      graph: data,
      container: 'container',
      settings: {
          defaultNodeColor: '#666',
          labelThreshold: 0
      }
  });

  var currentNode= s.graph.nodes("n0");

  // user has clicked a node
  s.bind('clickNode', function(e) {

    var nodeId = e.data.node.id;

    toKeep = s.graph.neighbors(nodeId);
    toKeep[nodeId] = e.data.node;
    var newNode = Math.random();
    // if (e.data.node.id == currentNode || currentNode == null) {
      // make the previous node and edge green to differentiate path
      e.data.node.color = '#696';
      e.data.node.size = 3;

      var next_node = e.data.node.label;
      console.log(next_node);

      s.graph.edges().forEach(function(e) {
          if(e.source == nodeId) {
              e.color = '#696';
          }
          else {
            e.color = '#ccc';
          }
      });

      // // add the new "main" node
      // s.graph.addNode({ id: newNode,
      //   "x": e.data.node.x + Math.random(),
      //   "y": e.data.node.x + Math.random(),
      //   "size": 5,
      //   "color": "#f00"});
      // s.graph.addEdge({
      //   id: newNode,
      //   source: newNode,
      //   target: e.data.node.id,
      // });
      var n = s.graph.nodes(e.data.node.id);

      // move camera to look at the new node
      sigma.misc.animation.camera(
        s.camera,
        {
          x: n[s.camera.readPrefix + 'x'],
          y: n[s.camera.readPrefix + 'y'],
          ratio: 1 // use 0.25 for best results on zoom
        },
        { duration: s.settings('animationsTime') }
      );
      s.refresh();
      var url_get = "http://127.0.0.1:8000/game/incomingnode/"+next_node;
      console.log(url_get);
      // use ajax to get the next set of nodes branching from this main node
      nextNodes(url_get, callback, n);
      currentNode = e.data.node.id;
  // }
});

  // Finally, update sigma
  s.refresh();

//////////////////// FUNCTIONS ///////////////////
function nextNodes(urlGet, callback, sourceNode) {
  $.ajax({
      url: urlGet,
      datatype: 'json',
      success: function(data) {
          callback(data, sourceNode);
      },
      failure: function(data) {
          alert('Something went wrong! Please try again.');
      }
    });
}
function callback(data, sourceNode) {
  // console.log(data);
  var json = JSON.parse(data);
  jQuery.each(json, function(i, val) {
    // alert(val["title"]);
    addNewNode(val, sourceNode);
  });
}

function addNewNode(obj, sourceNode) {
  newNode = Math.random();
  console.log(sourceNode.id);
  console.log(obj["title"]);
  s.graph.addNode({ id: newNode,
    "x": sourceNode.x + Math.random(),
    "y": sourceNode.y + Math.random(),
    "label": obj["title"],
    "size": 5,
    "color": "#666"});
  s.graph.addEdge({
    id: newNode,
    source: newNode,
    target: sourceNode.id,
  });
  s.refresh();
}
