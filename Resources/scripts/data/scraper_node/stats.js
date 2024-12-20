const got = require('got')
const { new_pokemons } = require('./new_pokemons.js')

class Pokemon {
    stats = {
        hp: {
            base: 0,
            ev: 0,
            index: 1
        },
        at: {
            base: 0,
            ev: 0,
            index: 2
        },
        de: {
            base: 0,
            ev: 0,
            index: 3
        },
        sa: {
            base: 0,
            ev: 0,
            index: 4
        },
        sd: {
            base: 0,
            ev: 0,
            index: 5
        },
        sp: {
            base: 0,
            ev: 0,
            index: 6
        }
    }
    id = ""
}

async function scrapePokemons(params) {
    try {
        const pokemons = []
        for (const new_pokemon of new_pokemons) {
            try {
                let pokemonToScrapeName = new_pokemon
                console.log(`Scraping ${pokemonToScrapeName}`)
                const response = await got(`https://bulbapedia.bulbagarden.net/w/api.php?action=parse&page=${pokemonToScrapeName}+(Pok%C3%A9mon)&prop=wikitext&format=json`).json()
                const wiki = response.parse.wikitext['*']
                const pokemon = new Pokemon
                pokemon.id = wiki.match(/ndex=(\d{3})/)[1]
                pokemon.stats.hp.base = wiki.match(/\|HP=(\d{1,3})/)[1]
                pokemon.stats.at.base = wiki.match(/\|Attack=(\d{1,3})/)[1]
                pokemon.stats.de.base = wiki.match(/\|Defense=(\d{1,3})/)[1]
                pokemon.stats.sa.base = wiki.match(/\|SpAtk=(\d{1,3})/)[1]
                pokemon.stats.sd.base = wiki.match(/\|SpDef=(\d{1,3})/)[1]
                pokemon.stats.sp.base = wiki.match(/\|Speed=(\d{1,3})/)[1]
                const evMatches = [...wiki.matchAll(/\|ev(\w{2})=(\d{1})/g)]
                evMatches.forEach(match => {
                    pokemon.stats[match[1]].ev = match[2]
                })
                pokemons.push(pokemon)
            } catch (error) {
                console.log(error)
            }
        }
        return pokemons
    } catch (error) {
        throw error
    }
}

function sortPokemon(a, b) {
    return a.id - b.id;
}

(async () => {
    try {
        const pokemons = await scrapePokemons()
        pokemons.sort(sortPokemon).forEach(pokemon => {
            Object.entries(pokemon.stats).forEach(([key, value]) => {
                console.log(`${pokemon.id},${value.index},${value.base},${value.ev}`)
            })
        })
    } catch (error) {
        console.log(error)
    }
})()
