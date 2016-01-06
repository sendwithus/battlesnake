export default makeNonGray = (rgb, DELTA) => {
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
}
