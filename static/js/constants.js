window.snakewithus = {
  MOVE_DELTA: 0,
  SQUARE_PADDING: 2,
  FOOD_SIZE: 0.5,
  HEAD_OPACITY: 1,
  BODY_OPACITY: 0.5,
  SQUARE_TYPES: {
    SNAKE: 'snake',
    SNAKE_HEAD: 'snake_head',
    FOOD: 'food'
  },
  DIRECTIONS: {
    NORTH: 'n',
    EAST: 'e',
    SOUTH: 's',
    WEST: 'w'
  },
  STATUS: {
    ALIVE: 'alive',
    DEAD: 'dead'
  },
  COLORS: {
    FOOD: '#F79E53',
    EMPTY: '#444'
  },
  MAX_COLOR: 255,
  MIN_COLOR: 120,
  BORDER_CHANGE: 4,
  KEYS: {
    UP: 38,
    DOWN: 40,
    LEFT: 37,
    RIGHT: 39
  }
};

window.generateColor = function() {
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
};

window.makeNonGray = function(rgb, DELTA) {
  DELTA = DELTA || 50;
  var rgbOld = rgb.slice(0);
  var rgbArr = [ 0, 1, 2 ];

  // Choose rand rgb segment for FIRST
  var randIndex = Math.floor(Math.random()*rgbArr.length);

  // Choose FIRST random color segment
  var RGBIndex1 = rgbArr.splice(randIndex, 1)[0];

  // Choose SECOND different color segment
  var RGBIndex2 = rgbArr[Math.floor(Math.random()*rgbArr.length)];

  // Choose before or after
  var newValue;
  var oldValue = rgb[RGBIndex1];
  if (Math.random() > oldValue / 255) {
    newValue = oldValue + DELTA;
    newValue = Math.min(255, newValue);
    var d = Math.min(255, (255 - (newValue + DELTA)));
    rgb[RGBIndex2] = rgb[RGBIndex1] + Math.floor(Math.random() * d);
  } else {
    newValue = oldValue - DELTA;
    newValue = Math.max(0, newValue);
    rgb[RGBIndex2] = Math.floor(Math.random() * newValue);
  }

  return rgb;
};

window.getURLParameter = function (name, defaultValue) {
  var val = decodeURI(
    (RegExp(name + '=' + '(.+?)(&|$)').exec(location.search)||[,null])[1]
  );

  if (val === 'null') {
    val = defaultValue;
  }
  return val;
};
