/*
This is an example snippet - you should consider tailoring it
to your service.
*/
/*
Add these to your `package.json`:
  "node-fetch": "^2.5.0"
*/

// Node doesn't implement fetch so we have to import it
const fetch =require("node-fetch");

async function fetchGraphQL(operationsDoc, operationName, variables) {
  const result = await fetch(
    "http://localhost:80/graphql/v1beta",
    {
      method: "POST",
      body: JSON.stringify({
        query: operationsDoc,
        variables: variables,
        operationName: operationName
      })
    }
  );

  return await result.json();
}

const operationsDoc = `
  query pokemon_details {
    species: pokemon_v2_pokemonspecies(where: {name: {_eq: "staryu"}}) {
      name
      base_happiness
      is_legendary
      is_mythical
      generation: pokemon_v2_generation {
        name
      }
      habitat: pokemon_v2_pokemonhabitat {
        name
      }
      pokemon: pokemon_v2_pokemons_aggregate(limit: 1) {
        nodes {
          height
          name
          id
          weight
          abilities: pokemon_v2_pokemonabilities_aggregate {
            nodes {
              ability: pokemon_v2_ability {
                name
              }
            }
          }
          stats: pokemon_v2_pokemonstats {
            base_stat
            stat: pokemon_v2_stat {
              name
            }
          }
          types: pokemon_v2_pokemontypes {
            slot
            type: pokemon_v2_type {
              name
            }
          }
          levelUpMoves: pokemon_v2_pokemonmoves_aggregate(where: {pokemon_v2_movelearnmethod: {name: {_eq: "level-up"}}}, distinct_on: move_id) {
            nodes {
              move: pokemon_v2_move {
                name
              }
              level
            }
          }
          pokemon_v2_encounters_aggregate {
            aggregate {
              count
            }
          }
          pokemon_v2_pokemonitems(where: {pokemon_v2_version: {name: {_eq: "firered"}}}) {
            pokemon_v2_item {
              name
              cost
            }
            rarity
          }
        }
      }
      flavorText: pokemon_v2_pokemonspeciesflavortexts(where: {pokemon_v2_language: {name: {_eq: "en"}}, pokemon_v2_version: {name: {_eq: "firered"}}}) {
        flavor_text
      }
    }
  }
`;

function fetchPokemon_details() {
  return fetchGraphQL(
    operationsDoc,
    "pokemon_details",
    {}
  );
}

async function startFetchPokemon_details() {
  const { errors, data } = await fetchPokemon_details();

  if (errors) {
    // handle those errors like a pro
    console.error(errors);
  }

  // do something great with this precious data
  console.log(data);
}

startFetchPokemon_details();