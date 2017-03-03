function placeNode(originNode, numNodes) {
  var radius = 0.5 // radius to place around node
  var x0 = originNode.x;
  var y0 = originNode.y;
  var alpha = (2*Math.PI)/numNodes;
  var firstX = x0 + (radius * Math.cos(alpha));
  var firstY = y0 + (radius * Math.sin(alpha));
  var nodeLocs = [{"x":firstX, "y":firstY}];

  for(i=1; i<numNodes; i++) {
    // increment alpha angle by adding 2pi/N
    alpha = alpha + ((2*Math.PI)/numNodes);
    var newX = x0 + (radius * Math.cos(alpha));
    var newY = y0 + (radius * Math.sin(alpha));
    nodeLocs.push({"x":newX, "y":newY});
  }
  nodeLocs.forEach(function(e) {
    alert("x: "+e.x+", y: "+e.y);
  });
}
