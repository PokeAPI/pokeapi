package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
)

type Operation struct {
	Query         string                 `json:"query"`
	Variables     map[string]interface{} `json:"variables"`
	OperationName string                 `json:"operationName"`
}

var (
	pokemonDetails = Operation{
		OperationName: "pokemon_details",
		Variables:     map[string]interface{}{
			"name": "staryu",
		},
		Query: `
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
	  `,
	}
)

func main() {
	url := "https://beta.pokeapi.co/graphql/v1beta"
	body, err := json.Marshal(pokemonDetails)
	if err != nil {
		log.Fatal(err)
	}

	resp, err := http.Post(url, "", bytes.NewReader(body))
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()
	body, err = ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(string(body))
}
