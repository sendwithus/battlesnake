export generateColor () {
  var color = [ ];
  for (var i=0; i<3; i++) {
    var c = Math.min(
      Math.max(
        snakewithus.MIN_COLOR, Math.floor(Math.random()*256
      )
    ), snakewithus.MAX_COLOR);
    color.push(c);
  }
  return color;
}
