package bulbapedia

import (
	"encoding/json"
	"net/http"
	"reflect"
	"regexp"
	"strconv"
	"strings"

	"github.com/rs/zerolog/log"
)

const (
	ErrID int64 = 20000
)

var Color = map[string]string{}

func getColor(color string) string {
	resp, err := http.Get("https://pokeapi.co/api/v2/pokemon-color/" + strings.ToLower(color))
	if err != nil {
		log.Fatal().
			Str("color", color).
			Err(err).
			Msg("Failed to fetch color")
	}
	defer resp.Body.Close()
	res := map[string]interface{}{}
	err = json.NewDecoder(resp.Body).Decode(&res)
	if err != nil {
		log.Fatal().
			Err(err).
			Msg("Failed to unmarshal JSON color response")
	}
	return strconv.Itoa(int(res["id"].(float64)))
}

func init() {
	for _, color := range []string{
		"black",
		"blue",
		"brown",
		"gray",
		"green",
		"pink",
		"purple",
		"red",
		"white",
		"yellow",
	} {
		Color[color] = getColor(color)
	}
}

func Unmarshal(data []byte, v interface{}) error {
	var st reflect.Type
	var ps reflect.Value
	switch rv := v.(type) {
	case *Species:
		st = reflect.TypeOf(*rv)
		ps = reflect.Indirect(reflect.ValueOf(rv))
		break
	case *Pokemon:
		st = reflect.TypeOf(*rv)
		ps = reflect.Indirect(reflect.ValueOf(rv))
		break
	}

	for i := 0; i < st.NumField(); i++ {
		field := st.Field(i)

		// bulbapedia
		if alias, ok := field.Tag.Lookup("bulbapedia"); ok {
			// Splits alias into bulbapedia:"[<key>][,<flag1>[,<flag2>]]"
			// round : converts float to int, rounds it and returns value as string
			// lower : lowercases string
			// color : converts to color id
			aliases := strings.Split(alias, ",")

			switch field.Type.Kind() {
			case reflect.Int, reflect.Int8, reflect.Int16, reflect.Int32, reflect.Int64:
				matches := regexp.MustCompile(`\|` + aliases[0] + `=(\d*)`).FindSubmatch(data)
				if len(matches) < 1 || string(matches[1]) == "" {
					ps.FieldByName(field.Name).SetInt(ErrID)
					break
				}
				res, err := strconv.ParseInt(string(matches[1]), 10, 64)
				if err != nil {
					ps.FieldByName(field.Name).SetInt(ErrID)
					break
				}
				ps.FieldByName(field.Name).SetInt(res)
				break
			default:
				matches := regexp.MustCompile(`\|` + aliases[0] + `=([^|\\n}]*)`).FindSubmatch(data)
				if len(matches) < 1 {
					// default values (only for string structs)
					if alias, ok := field.Tag.Lookup("default"); ok {
						ps.FieldByName(field.Name).SetString(alias)
					} else {
						ps.FieldByName(field.Name).SetString("")
					}
					break
				}
				res := strings.TrimSpace(string(matches[1]))
				for _, al := range aliases {
					switch al {
					case "lower":
						res = strings.ToLower(res)
						break
					case "color":
						res = Color[strings.ToLower(res)]
						break
					case "round":
						round, err := strconv.ParseFloat(string(matches[1]), 64)
						if err != nil {
							res = ""
						}
						res = strconv.Itoa(int(round * 10))
						break
					}
				}
				ps.FieldByName(field.Name).SetString(res)
				break
			}
		} else {
			// Non bulbapedia tags
			if alias, ok := field.Tag.Lookup("default"); ok {
				ps.FieldByName(field.Name).SetString(alias)
			}
		}
	}
	return nil
}
