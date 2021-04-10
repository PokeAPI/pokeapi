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
      species: pokemon_v2_pokemonspecies(where: {name: {_eq: $name}}) {
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
            foundInAsManyPlaces: pokemon_v2_encounters_aggregate {
              aggregate {
                count
              }
            }
            fireRedItems: pokemon_v2_pokemonitems(where: {pokemon_v2_version: {name: {_eq: "firered"}}}) {
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
