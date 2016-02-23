var getURLParameter = (name, defaultValue) => {
  var val = decodeURI(
    (RegExp(name + '=' + '(.+?)(&|$)').exec(location.search)||[,null])[1]
  );

  if (val === 'null') {
    val = defaultValue;
  }

  return val;
}
export default getURLParameter;
