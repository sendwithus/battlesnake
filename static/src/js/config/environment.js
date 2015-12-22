const env = {
  gaId: null,
};

if (process.env.NODE_ENV === "production") {
  env.gaId = "UA-67530875-1";
}

export default env;
