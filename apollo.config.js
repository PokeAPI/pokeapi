module.exports = {
  client: {
    service: {
      name: "pokeapi",
      url: "http://localhost:8080/v1/graphql",
      headers: {
        "x-hasura-admin-secret": "pokemon",
      },
    },
  },
};
