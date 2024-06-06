package bulbapedia

import (
	"bufio"
	"encoding/csv"
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"os"
	"sort"
	"strconv"

	"github.com/rs/zerolog/log"
)

type Pokemon struct {
	ID         int64  `json:"id" bulbapedia:"ndex"`
	Species    string `json:"species_id" bulbapedia:"ndex"`
	Identifier string `json:"identifier" bulbapedia:"name,lower"`
	Height     string `json:"height" bulbapedia:"height-m,round"`
	Weight     string `json:"weight" bulbapedia:"weight-kg,round"`
	Basexp     string `json:"expyield" bulbapedia:"expyield"`
	Order      string `json:"order"`
	Isdefault  string `json:"is_default" default:"1"`
}

type PokemonScrapper struct {
	Data map[int64]Pokemon
}

func (ps *PokemonScrapper) init() {
	ps.Data = make(map[int64]Pokemon)
}

func (ps *PokemonScrapper) read(path string) error {
	var err error
	file, err := os.Open(path)
	if err != nil {
		return err
	}
	defer file.Close()
	reader := csv.NewReader(file)
	reader.Read()
	for {
		row, err := reader.Read()
		if err != nil {
			if err == io.EOF {
				break
			}

			if err != nil {
				return err
			}
		}
		p := Pokemon{
			Identifier: row[1],
			Species:    row[2],
			Height:     row[3],
			Weight:     row[4],
			Basexp:     row[5],
			Order:      row[6],
			Isdefault:  row[7],
		}
		if row[0] == "" {
			p.ID = ErrID
		} else {
			if p.ID, err = strconv.ParseInt(row[0], 10, 64); err != nil {
				return err
			}
		}
		ps.Data[p.ID] = p
		log.Info().Str("pokemon_id", p.Identifier).Msg("Added pokemon")
	}
	return nil
}

func (ps *PokemonScrapper) scrape(name string) {
	fmt.Printf("Scrapping for %s\n", name)
	resp, err := http.Get("https://bulbapedia.bulbagarden.net/w/api.php?action=parse&page=" + name + "&prop=wikitext&format=json")
	if err != nil {
		log.Fatal().Err(err)
	}
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	pokemon := &Pokemon{}
	if err := Unmarshal(body, pokemon); err != nil {

	}
	pokemon.Species = strconv.Itoa(int(pokemon.ID))
	if _, ok := ps.Data[pokemon.ID]; ok {
		fmt.Printf("Updating old pokemon %s [%d]\n", pokemon.Identifier, pokemon.ID)
	}
	ps.Data[pokemon.ID] = *pokemon
}

func (ps *PokemonScrapper) write(path string) error {
	file, err := os.Create(path)
	if err != nil {
		return err
	}
	defer file.Close()

	w := bufio.NewWriter(file)
	fmt.Fprintln(w, "id,identifier,species_id,height,weight,base_experience,order,is_default")

	keys := make([]int, 0, len(ps.Data))
	for k := range ps.Data {
		keys = append(keys, int(k))
	}
	sort.Ints(keys)

	for _, k := range keys {
		pokemon := ps.Data[int64(k)]
		fmt.Fprintf(w, "%d,%s,%s,%s,%s,%s,%s,%s\n", pokemon.ID, pokemon.Identifier, pokemon.Species, pokemon.Height, pokemon.Weight, pokemon.Basexp, pokemon.Order, pokemon.Isdefault)
	}

	return w.Flush()
}
