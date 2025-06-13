/*
Get's many details about a pokemon passed as argument (starmie as default).

It gets:
  - happiness
  - if legendary/mythical
  - generation
  - habitat
  - height
  - weight
  - ID
  - abilities
  - stats
  - types
  - learnable moves by leveling up
  - in how many locations it can be found
  - holdable items in Fire Red
  - flavor text
*/

const fetch = require("node-fetch")

async function fetchGraphQL(query, variables, operationName) {
  const result = await fetch(
    "https://beta.pokeapi.co/graphql/v1beta",
    {
      method: "POST",
      body: JSON.stringify({
        query: query,
        variables: variables,
        operationName: operationName
      })
    }
  )

  return await result.json()
}



function fetchPokemon_details(name="starmie") {
  const query = `
    query pokemon_details($name: String) {
      species: pokemonspecies(where: {name: {_eq: $name}}) {
        name
        base_happiness
        is_legendary
        is_mythical
        generation: generation {
          name
        }
        habitat: pokemonhabitat {
          name
        }
        pokemon: pokemons_aggregate(limit: 1) {
          nodes {
            height
            name
            id
            weight
            abilities: pokemonabilities_aggregate {
              nodes {
                ability: ability {
                  name
                }
              }
            }
            stats: pokemonstats {
              base_stat
              stat: stat {
                name
              }
            }
            types: pokemontypes {
              slot
              type: type {
                name
              }
            }
            levelUpMoves: pokemonmoves_aggregate(where: {movelearnmethod: {name: {_eq: "level-up"}}}, distinct_on: move_id) {
              nodes {
                move: move {
                  name
                }
                level
              }
            }
            foundInAsManyPlaces: encounters_aggregate {
              aggregate {
                count
              }
            }
            fireRedItems: pokemonitems(where: {version: {name: {_eq: "firered"}}}) {
              item {
                name
                cost
              }
              rarity
            }
          }
        }
        flavorText: pokemonspeciesflavortexts(where: {language: {name: {_eq: "en"}}, version: {name: {_eq: "firered"}}}) {
          flavor_text
        }
      }
    }
  `

  return fetchGraphQL(
    query,
    {"name": name},
    "pokemon_details"
  )
}

async function main() {
  const pokemon = process.argv.slice(2)[0];
  const { errors, data } = await fetchPokemon_details(pokemon)
  if (errors) {
    console.error(errors)
  }
  console.log(JSON.stringify(data, null, 2))
}

main()
