package bulbapedia

import (
	"bufio"
	"os"

	"github.com/rs/zerolog/log"
)

type Scrapper interface {
	init()
	read(path string) error
	scrape(name string)
	write(path string) error
}

func Scrape(s Scrapper, source, newPokemon, out string) {
	s.init()
	s.read(source)

	sl := fetchList(newPokemon)
	for _, n := range sl {
		s.scrape(n)
	}
	s.write(out)
}

func fetchList(path string) []string {
	file, err := os.Open(path)
	if err != nil {
		log.Fatal().Err(err).Str("path", path).Msg("Failed to open file @")
	}
	defer file.Close()

	sl := []string{}
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		sl = append(sl, scanner.Text())
	}
	return sl
}
