package bulbapedia

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"testing"

	"github.com/anaskhan96/soup"
)

func TestPokemonUnmarshal(t *testing.T) {
	v := &Pokemon{}
	resp, _ := http.Get("https://bulbapedia.bulbagarden.net/w/api.php?action=parse&page=Rolycoly_(Pok%C3%A9mon)&prop=wikitext&format=json")
	body, _ := ioutil.ReadAll(resp.Body)
	Unmarshal(body, v)
	fmt.Printf("%+v\n", v)
}

func TestSpeciesUnmarshal(t *testing.T) {
	v := &Species{}
	resp, _ := soup.Get("https://bulbapedia.bulbagarden.net/w/index.php?title=Rolycoly_(Pok%C3%A9mon)&action=edit")
	body := []byte(soup.HTMLParse(resp).Find("textarea", "id", "wpTextbox1").Text())
	Unmarshal(body, v)
	fmt.Printf("%+v\n", v)
}
