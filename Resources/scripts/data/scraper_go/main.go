package main

import (
	"scraper/pkg/bulbapedia"
)

func main() {
	bulbapedia.Scrape(&bulbapedia.PokemonScrapper{}, "data/pokemon.csv", "data/new_pokemon.txt", "out/pokemon.csv")
	bulbapedia.Scrape(&bulbapedia.SpeciesScrapper{}, "data/pokemon_species.csv", "data/new_pokemon.txt", "out/pokemon_species.csv")
}
