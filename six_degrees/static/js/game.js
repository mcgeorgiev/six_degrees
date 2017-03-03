var startData;
var urlStart = "http://127.0.0.1:8000/game/start";
var s;
var allNodes = [];
var nodeList = [];

/////////////////////// GET STARTING DATA ///////////////////////////
function getStartData() {
    $.ajax({
    url: urlStart,
    datatype: 'json',
    success: function(data) {
        var jsonResp = JSON.parse(data);
        if(jsonResp["code"] == 500) {
            alert("FAIL");
        }
        startData = JSON.parse(data);
        startSigma();
    },
    failure: function(data) {
        alert('Something went wrong! Please try again.');
    }
  });
}
/////////////////////// START SIGMA STUFF ///////////////////////////
var  NUMBER_OF_NODES;
function startSigma() {
  console.log(startData.start);

  NUMBER_OF_NODES = Object.keys(startData.related).length;
  console.log(NUMBER_OF_NODES);
  new sigma.classes.configurable(
    {
      autoRescale: false,
      autoResize: false,
      singleHover: true,
      defaultLabelSize: 20,
      fontStyle: "bold",
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
    s = new sigma({
        container: 'container',
        settings: {
            defaultNodeColor: '#666',
            labelThreshold: 4,
            singleHover: true,
            defaultLabelSize: 13,
            fontStyle: "bold",
            defaultNodeHoverColor: "#696",
        }
    });
    cam = s.addCamera();

    // make a node from the "start" node
    s.graph.addNode({
      "id": startData.start.id,
      "label": startData.start.name,
      "x": 0,
      "y": 0,
      "size": 8,
      "color": "#ccc",
    });
    var currentNode= s.graph.nodes(startData.start.id);
    nodeList = [startData.start.id];
    allNodes.push(startData.start.id);
    var endNode = startData.end;

    $("#goal").text("Goal: "+endNode.name);
    // add the rest of the nodes
    var nodeLocs = newNodeXY(currentNode, NUMBER_OF_NODES);
    $.each(startData.related, function(i, val) {
      addNewNode(val, currentNode, nodeLocs[i].x, nodeLocs[i].y);
      allNodes.push(val.id);
    });
    // user has clicked a node
    s.bind('clickNode', function(e) {

      var nodeId = e.data.node.id;
      nodeList.push(nodeId);

      if(nodeId == endNode.id) {
        // game is over, post nodeList to server and tell user they won
        $("#goal").text("You won the game! It took "+nodeList.length-1+" clicks!");
        $("#result").text("List: ");
        nodeList.forEach(function(n) {
          $("#result").append("<li>"+n+"</li>")
        });
        $("#container").css("opacity", 0.1);
        $.post("http://127.0.0.1:8000/game/gameover/", nodeList);
        return;
      }


      toKeep = s.graph.neighbors(nodeId);
      toKeep[nodeId] = e.data.node;
      var newNode = Math.random();
      // if (e.data.node.id == currentNode || currentNode == null) {
      s.graph.nodes().forEach(function(n) {
          n.color = '#ccc';
          n.size = 1;
      });
      s.graph.edges().forEach(function(e) {
          e.color = '#ccc';
          var pos = nodeList.indexOf(e.source);
          if(pos > 0) {
              e.color = '#696';
              s.graph.nodes(nodeList[pos]).color = '#696';
              e.size = 8;
          }
      });
      // make the previous node and edge green to differentiate path
      e.data.node.color = '#696';
      e.data.node.size = 3;

      var next_node = e.data.node.label;

      var n = s.graph.nodes(e.data.node.id);

      // move camera to look at the new node
      cam.goTo({
        x: n.x,
        y: n.y,
        ratio: 0.77, //zoom ratio
        angle: 0,
      });

      s.refresh();

      var url_get = "http://127.0.0.1:8000/game/incomingnode/"+next_node;

      // use ajax to get the next set of nodes branching from this main node
      nextNodes(url_get, callback, n);
      currentNode = e.data.node.id;
  });

    // Finally, update sigma
    s.refresh();
}
//////////////////// FUNCTIONS ///////////////////
function nextNodes(urlGet, callback, sourceNode) {
  $.ajax({
      url: urlGet,
      datatype: 'json',
      success: function(data) {
          var jsonResp = JSON.parse(data);
          if(jsonResp["code"] == 500) {
              gameOver();
          }
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
  var nodeLocs = newNodeXY(sourceNode, Object.keys(json).length);
  jQuery.each(json, function(i, val) {
    // alert(val["title"]);
    var pos = allNodes.indexOf(val.id);
    console.log(allNodes);
    console.log(pos);
    if(pos == -1) {
      addNewNode(val, sourceNode, nodeLocs[i].x, nodeLocs[i].y);
    }
  });
}

function addNewNode(obj, sourceNode, x, y) {
  newNode = obj.id;

  s.graph.addNode({ id: obj.id,
    "x": x,
    "y": y,
    "label": obj.name,
    "size": 5,
    "color": "#666"});
  s.graph.addEdge({
    id: newNode,
    source: newNode,
    target: sourceNode.id,
  });
  s.refresh();
  allNodes.push(newNode);
}

function newNodeXY(originNode, numNodes) {
  var radius = [0.7, 1, 0.55, 0.82, 0.52] // radius to place around node
  var x0 = originNode.x;
  var y0 = originNode.y;
  var alpha = (1.8*Math.PI)/(numNodes+1);
  console.log(alpha);
  var firstX = x0 + (1 * Math.cos(alpha));
  var firstY = y0 + (1 * Math.sin(alpha));
  var nodeLocs = [{"x":firstX, "y":firstY}];

  for(i=0; i<numNodes; i++) {
    // increment alpha angle by adding 2pi/N
    var rad = Math.floor(Math.random()*radius.length);
    alpha = alpha + ((2*Math.PI)/(numNodes+1));
    console.log(alpha);
    var newX = x0 + (radius[rad] * Math.cos(alpha));
    var newY = y0 + (radius[rad] * Math.sin(alpha));
    nodeLocs.push({"x":newX, "y":newY});
  }
  // nodeLocs.forEach(function(e) {
  //   alert("x: "+e.x+", y: "+e.y);
  // });
  return nodeLocs;
}

function gameOver() {
  $("#goal").text("You lost after "+nodeList.length-1+" clicks!");
  $("#result").text("List: ");
  nodeList.forEach(function(n) {
    $("#result").append("<li>"+n+"</li>")
  });
}
