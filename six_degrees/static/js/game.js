var startData;
var baseUrl = "";
var s;
var allNodes = [];
var visitedNodes = {};
visitedNodes['nodes'] = [];
var endNode;

/////////////////////// GET STARTING DATA ///////////////////////////
function getStartData() {
    $.ajax({
    url: baseUrl + "start/",
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
/////////////////////// START SIGMA ///////////////////////////
var  NUMBER_OF_NODES;
function startSigma() {
  console.log(startData.start);

  // alert(getCookie('csrftoken'));

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

    allNodes.push(startData.start.id);
    endNode = startData.end;

    // show some game details on screen
    $("#gameoverlay").html(
        "<h3>Your goal is to link</h3><h1><strong>"+startData.start.name+"</strong></h1>"+
        " and <h1><strong>"+endNode.name+"</strong></h1>"+
        "<h3> Click the first node when it appears to begin.</h3>");
    $("#gameoverlay").delay( 2500 ).fadeOut(400);
    $("#gameoverlay").promise().done(function() {
        $("#goal").html("Goal: <strong>"+endNode.name+"</strong>");
        $("#goal").css("opacity", 1);
        $("#clicks").css("opacity", 1);
    });
    var isClickable = true;
    // user has clicked a node
    s.bind('clickNode', function(e) {

      if(isClickable) {

          var clicks = Object.keys(visitedNodes["nodes"]).length;
          // update click counter in UI
          $("#clicks").html("<small>clicks: </small>"+clicks);

          var nodeId = e.data.node.id;
          visitedNodes.nodes.push({
                        "id": e.data.node.id,
                        "label": e.data.node.label
                    });
          if(nodeId == endNode.id) {
            isClickable = false;
            // game has been won
            gameWin();
            return;
          }

          //************************TESTING
          //************************TESTING
          if(clicks == 4) {
              isClickable = false;
              gameWin();
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
            //   var pos = visitedNodes.indexOf(e.source);
            //   if(pos > 0) {
            //       e.color = '#696';
            //     //   s.graph.nodes(visitedNodes[pos]).color = '#696';
            //       e.size = 8;
            //   }
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

          var url_post = baseUrl+"incomingnode/"+next_node+"/";

          // use ajax to get the next set of nodes branching from this main node
          nextNodes(url_post, callback, n);
          currentNode = e.data.node.id;
        }
    });

        // Finally, update sigma
        s.refresh();
}
//////////////////// FUNCTIONS ///////////////////
function nextNodes(urlPost, callback, sourceNode) {
  $.ajax({
      url: urlPost,
      datatype: 'json',
      method: 'POST',
      data: {"csrfmiddlewaretoken":getCookie('csrftoken'), "endNode":endNode},
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
    if(pos == -1) {
      addNewNode(val, sourceNode, nodeLocs[i].x, nodeLocs[i].y);
  } else {
      // node already exists, create a link back to it
      addNewEdge(val, sourceNode);
      // and make the node big again
      s.graph.nodes(val.id).size = 5;
      s.graph.nodes(val.id).color = "#666";
  }
  s.refresh();
  });
}

// add a new node to the graph and call create an edge
function addNewNode(obj, sourceNode, x, y) {

  s.graph.addNode({ id: obj.id,
    "x": x,
    "y": y,
    "label": obj.name,
    "size": 5,
    "color": "#666"});
  addNewEdge(obj, sourceNode);
  s.refresh();
  allNodes.push(obj.id);
}

// adds an edge between two nodes
function addNewEdge(newNode, existNode) {
    console.log(newNode.id);
    console.log(existNode.id);
    // random edge ID
    s.graph.addEdge({
      id: Math.floor(Math.random()*1e10),
      source: existNode.id,
      target: newNode.id,
    });
}

// calculates the X and Y positions to position the new nodes around the source
function newNodeXY(originNode, numNodes) {
  var radius = [0.7, 0.6, 0.63, 0.82, 0.52] // radius to place around node
  var x0 = originNode.x;
  var y0 = originNode.y;
  var alpha = (1.8*Math.PI)/(numNodes+1);

  var firstX = x0 + (1 * Math.cos(alpha));
  var firstY = y0 + (1 * Math.sin(alpha));
  var nodeLocs = [{"x":firstX, "y":firstY}];

  for(i=0; i<numNodes; i++) {
    // increment alpha angle by adding 2pi/N
    var rad = Math.floor(Math.random()*radius.length);
    alpha = alpha + ((2*Math.PI)/(numNodes+1));

    var newX = x0 + (radius[rad] * Math.cos(alpha));
    var newY = y0 + (radius[rad] * Math.sin(alpha));
    nodeLocs.push({"x":newX, "y":newY});
  }
  // nodeLocs.forEach(function(e) {
  //   alert("x: "+e.x+", y: "+e.y);
  // });
  return nodeLocs;
}

// game has been lost
function gameOver() {
    var clicks = Object.keys(visitedNodes["nodes"]).length - 1 ;
    clickTxt = (clicks > 1) ? "clicks":"click";
    $("#gameoverlay").html("<h1>Game over! You hit a dead link.</h1><h2>"+clicks+" "+clickTxt+"</h2>");
    jQuery.each(visitedNodes["nodes"], function(i, val) {
      if(i < clicks) {
          $("#gameoverlay").append(val.label+' <span class="glyphicon glyphicon-triangle-right"></span> ')
      } else {
          $("#gameoverlay").append('<strong>'+val.label+'</strong>');
      }
    })
    $("#gameoverlay").append(
        '<div class="text-center"><div class="btn-group">'+
        '<a class="btn btn-info btn-lg" href="#">View Graph</a>'+
        '<a class="btn btn-info btn-lg" href="../game/">Play Again</a>'+
        '<a class="btn btn-info btn-lg" href="../">Exit</a>'+
        '</div></div>'
    );
    $("#gameoverlay").fadeIn(400);
}

// function to get value of a given cookie
function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}

// game has been won
function gameWin() {
    gameOverNodeList = JSON.stringify(visitedNodes["nodes"], null, 2); // Indented 4 spaces
    // $.post(baseUrl + "gameover/", {"nodes":gameOverNodeList, "csrfmiddlewaretoken":getCookie('csrftoken')});
    $.ajax({
        url: baseUrl + "gameover/",
        datatype: 'json',
        type: 'POST',
        method: 'POST',
        data: {
            "nodes":gameOverNodeList,
            "csrfmiddlewaretoken":getCookie('csrftoken')
        },
        success: function(resp) {
            var jsonResp = JSON.parse(resp);
            if(jsonResp["code"] == 500) {
                gameOver();
            }
            alert("GOT IT");
            alert(resp);
        },
        failure: function(resp) {
            alert('Something went wrong! Please try again.');
        }
      });

    // game is over, post visitedNodes to server and tell user they won
    var clicks = Object.keys(visitedNodes["nodes"]).length - 1 ;
    clickTxt = (clicks > 1) ? "clicks":"click";
    $("#gameoverlay").html("<h1>You won the game!</h1><h2>"+clicks+" "+clickTxt+"</h2>");
    jQuery.each(visitedNodes["nodes"], function(i, val) {
      if(i < clicks) {
          $("#gameoverlay").append(val.label+' <span class="glyphicon glyphicon-triangle-right"></span> ')
      } else {
          $("#gameoverlay").append('<strong>'+val.label+'</strong>');
      }
    })
    $("#gameoverlay").append(
        '<div class="text-center"><div class="btn-group">'+
        '<a class="btn btn-info btn-lg" href="#">View Graph</a>'+
        '<a class="btn btn-info btn-lg" href="../game/">Play Again</a>'+
        '<a class="btn btn-info btn-lg" href="../game/dashboard">Exit</a>'+
        '</div></div>'
    );
    $("#gameoverlay").fadeIn(400);
}
