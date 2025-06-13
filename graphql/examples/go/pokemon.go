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
