
# Pokeapi V2 API Reference

<table class="hide">
  <tbody>
    <tr>
      <th colspan="3">API Endpoints</th>
    </tr>
    <tr>
      <td>
				<ul>
					<li><a href="#abilities">Abilities</a></li>
					<li><a href="#berries">Berries</a></li>
					<li><a href="#berry-firmnesses">Berry Firmnesses</a></li>
					<li><a href="#berry-flavors">Berry Flavors</a></li>
					<li><a href="#characteristics">Characteristics</a></li>
					<li><a href="#contest-types">Contest Types</a></li>
					<li><a href="#contest-effects">Contest Effects</a></li>
					<li><a href="#egg-groups">Egg Groups</a></li>
					<li><a href="#encounter-methods">Encounter Methods</a></li>
					<li><a href="#encounter-conditions">Encounter Conditions</a></li>
					<li><a href="#encounter-condition-values">Encounter Condition Values</a></li>
					<li><a href="#evolution-chains">Evolution Chains</a></li>
					<li><a href="#evolution-triggers">Evolution Triggers</a></li>
					<li><a href="#generations">Generations</a></li>
					<li><a href="#genders">Genders</a></li>
					<li><a href="#growth-rates">Growth Rates</a></li>
				</ul>
      </td>
      <td>
				<ul>
					<li><a href="#items">Items</a></li>
					<li><a href="#item-categories">Item Categories</a></li>
					<li><a href="#item-attributes">Item Attributes</a></li>
					<li><a href="#item-fling-effects">Item Fling Effects</a></li>
					<li><a href="#item-pockets">Item Pockets</a></li>
					<li><a href="#languages">Languages</a></li>
					<li><a href="#locations">Locations</a></li>
					<li><a href="#location-areas">Location Areas</a></li>
					<li><a href="#machines">Machines</a></li>
					<li><a href="#moves">Moves</a></li>
					<li><a href="#move-ailments">Move Ailments</a></li>
					<li><a href="#move-battle-styles">Move Battle Styles</a></li>
					<li><a href="#move-categories">Move Categories</a></li>
					<li><a href="#move-damage-classes">Move Damage Classes</a></li>
					<li><a href="#move-learn-methods">Move Learn Methods</a></li>
					<li><a href="#move-targets">Move Targets</a></li>
				</ul>
      </td>
      <td>
				<ul>
					<li><a href="#natures">Natures</a></li>
					<li><a href="#pal-park-areas">Pal Park Areas</a></li>
					<li><a href="#pokedexes">Pokédexes</a></li>
					<li><a href="#pokemon">Pokémon</a></li>
					<li><a href="#pokemon-colors">Pokémon Colors</a></li>
					<li><a href="#pokemon-forms">Pokémon Forms</a></li>
					<li><a href="#pokemon-habitats">Pokémon Habitats</a></li>
					<li><a href="#pokemon-shapes">Pokémon Shapes</a></li>
					<li><a href="#pokemon-species">Pokémon Species</a></li>
					<li><a href="#pokeathlon-stats">Pokéathlon Stats</a></li>
					<li><a href="#regions">Regions</a></li>
					<li><a href="#stats">Stats</a></li>
					<li><a href="#super-contest-effects">Super Contest Effects</a></li>
					<li><a href="#types">Types</a></li>
					<li><a href="#version">Versions</a></li>
					<li><a href="#version-groups">Version Groups</a></li>
				</ul>
      </td>
    </tr>
  </tbody>
</table>

## Resource Lists
Calling any API endpoint without a resource ID or name will return a paginated list of available resources for that API. By default, a list 'page' will contain up to 20 resources. If you would like to change this just add a 'limit' query param, e.g. `limit=60`.

### GET api/v2/{endpoint}

###### Example response for unnamed resources

```json
{
	"count": 365,
	"next": "http://pokeapi.co/api/v2/evolution-chain/?limit=20&offset=20",
	"previous": null,
	"results": [{
		"url": "http://pokeapi.co/api/v2/evolution-chain/1/"
	}]
}
```

#### APIResourceList

| Name     | Description                                           | Data Type                        |
|:---------|:------------------------------------------------------|:---------------------------------|
| count    | The total number of resources available from this API | integer                          |
| next     | The URL for the next page in the list                 | string                           |
| previous | The URL for the previous page in the list             | boolean                          |
| results  | A list of unnamed API resources                       | list [APIResource](#apiresource) |

###### Example response for named resources

```json
{
	"count": 248,
	"next": "http://pokeapi.co/api/v2/ability/?limit=20&offset=20",
	"previous": null,
	"results": [{
		"name": "stench",
		"url": "http://pokeapi.co/api/v2/ability/1/"
	}]
}
```

#### NamedAPIResourceList

| Name     | Description                                           | Data Type                                  |
|:---------|:------------------------------------------------------|:-------------------------------------------|
| count    | The total number of resources available from this API | integer                                    |
| next     | The URL for the next page in the list                 | string                                     |
| previous | The URL for the previous page in the list             | boolean                                    |
| results  | A list of named API resources                         | list [NamedAPIResource](#namedapiresource) |

<h1 id="berries-section">Berries</h1>

## Berries
Berries are small fruits that can provide HP and status condition restoration, stat enhancement, and even damage negation when eaten by Pokémon. Check out [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Berry) for greater detail.

### GET api/v2/berry/{id or name}

###### Example response

```json
{
	"id": 1,
	"name": "cheri",
	"growth_time": 3,
	"max_harvest": 5,
	"natural_gift_power": 60,
	"size": 20,
	"smoothness": 25,
	"soil_dryness": 15,
	"firmness": {
		"name": "soft",
		"url": "http://pokeapi.co/api/v2/berry-firmness/2/"
	},
	"flavors": [{
		"potency": 10,
		"flavor": {
			"name": "spicy",
			"url": "http://pokeapi.co/api/v2/berry-flavor/1/"
		}
	}],
	"item": {
		"name": "cheri-berry",
		"url": "http://pokeapi.co/api/v2/item/126/"
	},
	"natural_gift_type": {
		"name": "fire",
		"url": "http://pokeapi.co/api/v2/type/10/"
	}
}

```

###### Response models

#### Berry

| Name               | Description                                                                                                                       | Data Type                                                                  |
|:-------------------|:----------------------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------|
| id                 | The identifier for this berry resource                                                                                            | integer                                                                    |
| name               | The name for this berry resource                                                                                                  | string                                                                     |
| growth_time        | Time it takes the tree to grow one stage, in hours. Berry trees go through four of these growth stages before they can be picked. | integer                                                                    |
| max_harvest        | The maximum number of these berries that can grow on one tree in Generation IV                                                    | integer                                                                    |
| natural_gift_power | The power of the move "Natural Gift" when used with this Berry                                                                    | integer                                                                    |
| size               | The size of this Berry, in millimeters                                                                                            | integer                                                                    |
| smoothness         | The smoothness of this Berry, used in making Pokéblocks or Poffins                                                                | integer                                                                    |
| soil_dryness       | The speed at which this Berry dries out the soil as it grows.  A higher rate means the soil dries more quickly.                   | integer                                                                    |
| firmness           | The firmness of this berry, used in making Pokéblocks or Poffins                                                                  | [NamedAPIResource](#namedapiresource) ([BerryFirmness](#berry-firmnesses)) |
| flavors            | A list of references to each flavor a berry can have and the potency of each of those flavors in regard to this berry             | list [BerryFlavorMap](#berryflavormap)                                     |
| item               | Berries are actually items. This is a reference to the item specific data for this berry.                                         | [NamedAPIResource](#namedapiresource) ([Item](#items))                     |
| natural_gift_type  | The type inherited by "Natural Gift" when used with this Berry                                                                    | [NamedAPIResource](#namedapiresource) ([Type](#types))                     |

#### BerryFlavorMap

| Name    | Description                                          | Data Type                                                             |
|:--------|:-----------------------------------------------------|:----------------------------------------------------------------------|
| potency | How powerful the referenced flavor is for this berry | integer                                                               |
| flavor  | The referenced berry flavor                          | [NamedAPIResource](#namedapiresource) ([BerryFlavor](#berry-flavors)) |

## Berry Firmnesses

### GET api/v2/berry-firmness/{id or name}

###### Example response

```json
{
	"id": 1,
	"name": "very-soft",
	"berries": [{
		"name": "pecha",
		"url": "http://pokeapi.co/api/v2/berry/3/"
	}],
	"names": [{
		"name": "Very Soft",
		"language": {
			"name": "en",
			"url": "http://pokeapi.co/api/v2/language/9/"
		}
	}]
}

```

###### Response models

#### BerryFirmness

| Name    | Description                                                   | Data Type                                                      |
|:--------|:--------------------------------------------------------------|:---------------------------------------------------------------|
| id      | The identifier for this berry firmness resource               | integer                                                        |
| name    | The name for this berry firmness resource                     | string                                                         |
| berries | A list of the berries with this firmness                      | list [NamedAPIResource](#namedapiresource) ([Berry](#berries)) |
| names   | The name of this berry firmness listed in different languages | list [Name](#resourcename)                                     |

## Berry Flavors
Flavors determine whether a Pokémon will benefit or suffer from eating a berry based on their [nature](#natures). Check out [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Flavor) for greater detail.

### GET api/v2/berry-flavor/{id or name}

###### Example response

```json
{
	"id": 1,
	"name": "spicy",
	"berries": [{
		"potency": 10,
		"berry": {
			"name": "rowap",
			"url": "http://pokeapi.co/api/v2/berry/64/"
		}
	}],
	"contest_type": {
		"name": "cool",
		"url": "http://pokeapi.co/api/v2/contest-type/1/"
	},
	"names": [{
		"name": "Spicy",
		"language": {
			"name": "en",
			"url": "http://pokeapi.co/api/v2/language/9/"
		}
	}]
}

```

###### Response models

#### BerryFlavor

| Name         | Description                                                 | Data Type                                                             |
|:-------------|:------------------------------------------------------------|:----------------------------------------------------------------------|
| id           | The identifier for this berry flavor resource               | integer                                                               |
| name         | The name for this berry flavor resource                     | string                                                                |
| berries      | A list of the berries with this flavor                      | list [FlavorBerryMap](#flavorberrymap)                                |
| contest_type | The contest type that correlates with this berry flavor     | [NamedAPIResource](#namedapiresource) ([ContestType](#contest-types)) |
| names        | The name of this berry flavor listed in different languages | list [Name](#resourcename)                                            |

#### FlavorBerryMap

| Name    | Description                                          | Data Type                                               |
|:--------|:-----------------------------------------------------|:--------------------------------------------------------|
| potency | How powerful the referenced flavor is for this berry | integer                                                 |
| berry   | The berry with the referenced flavor                 | [NamedAPIResource](#namedapiresource) ([Berry](#berry)) |

<h1 id="contests-section">Contests</h1>

## Contest Types
Contest types are categories judges used to weigh a Pokémon's condition in Pokémon contests. Check out [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Contest_condition) for greater detail.

### GET api/v2/contest-type/{id or name}

###### Example response

```json
{
	"id": 1,
	"name": "cool",
	"berry_flavor": {
		"name": "spicy",
		"url": "http://pokeapi.co/api/v2/berry-flavor/1/"
	},
	"names": [{
		"name": "Cool",
		"color": "Red",
		"language": {
			"name": "en",
			"url": "http://pokeapi.co/api/v2/language/9/"
		}
	}]
}

```

###### Response models

#### ContestType

| Name         | Description                                                 | Data Type                                                             |
|:-------------|:------------------------------------------------------------|:----------------------------------------------------------------------|
| id           | The identifier for this contest type resource               | integer                                                               |
| name         | The name for this contest type resource                     | string                                                                |
| berry_flavor | The berry flavor that correlates with this contest type     | [NamedAPIResource](#namedapiresource) ([BerryFlavor](#berry-flavors)) |
| names        | The name of this contest type listed in different languages | list [ContestName](#contestname)                                      |

#### ContestName

| Name     | Description                                   | Data Type                                                     |
|:---------|:----------------------------------------------|:--------------------------------------------------------------|
| name     | The name for this contest                     | string                                                        |
| color    | The color associated with this contest's name | string                                                        |
| language | The language that this name is in             | [NamedAPIResource](#namedapiresource) ([Language](#language)) |

## Contest Effects
Contest effects refer to the effects of moves when used in contests.

### GET api/v2/contest-effect/{id}

###### Example response

```json
{
	"id": 1,
	"appeal": 4,
	"jam": 0,
	"effect_entries": [{
		"effect": "Gives a high number of appeal points wth no other effects.",
		"language": {
			"name": "en",
			"url": "http://pokeapi.co/api/v2/language/9/"
		}
	}],
	"flavor_text_entries": [{
		"flavor_text": "A highly appealing move.",
		"language": {
			"name": "en",
			"url": "http://pokeapi.co/api/v2/language/9/"
		}
	}]
}

```

###### Response models

#### ContestEffect

| Name                | Description                                                          | Data Type                      |
|:--------------------|:---------------------------------------------------------------------|:-------------------------------|
| id                  | The identifier for this contest type resource                        | integer                        |
| appeal              | The base number of hearts the user of this move gets                 | integer                        |
| jam                 | The base number of hearts the user's opponent loses                  | integer                        |
| effect_entries      | The result of this contest effect listed in different languages      | list [Effect](#effect)         |
| flavor_text_entries | The flavor text of this contest effect listed in different languages | list [FlavorText](#flavortext) |

## Super Contest Effects
Super contest effects refer to the effects of moves when used in super contests.

### GET api/v2/super-contest-effect/{id}

###### Example response

```json
{
	"id": 1,
	"appeal": 2,
	"flavor_text_entries": [{
		"flavor_text": "Enables the user to perform first in the next turn.",
		"language": {
			"name": "en",
			"url": "http://pokeapi.co/api/v2/language/9/"
		}
	}],
	"moves": [{
		"name": "agility",
		"url": "http://pokeapi.co/api/v2/move/97/"
	}]
}
```

###### Response models

#### SuperContestEffect

| Name                | Description                                                                | Data Type                                                   |
|:--------------------|:---------------------------------------------------------------------------|:------------------------------------------------------------|
| id                  | The identifier for this super contest effect resource                      | integer                                                     |
| appeal              | The level of appeal this super contest effect has                          | integer                                                     |
| flavor_text_entries | The flavor text of this super contest effect listed in different languages | list [FlavorText](#flavortext)                              |
| moves               | A list of moves that have the effect when used in super contests           | list [NamedAPIResource](#namedapiresource) ([Move](#moves)) |

<h1 id="encounters-section">Encounters</h1>

## Encounter Methods
Methods by which the player might can encounter Pokémon in the wild, e.g., walking in tall grass. Check out [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Wild_Pokémon) for greater detail.

### GET api/v2/encounter-method/{id or name}

###### Example response

```json
{
	"id": 1,
	"name": "walk",
	"order": 1,
	"names": [{
		"name": "Walking in tall grass or a cave",
		"language": {
			"name": "en",
			"url": "http://pokeapi.co/api/v2/language/9/"
		}
	}]
}

```

###### Response models

#### EncounterMethod

| Name  | Description                                                     | Data Type                  |
|:------|:----------------------------------------------------------------|:---------------------------|
| id    | The identifier for this encounter method resource               | integer                    |
| name  | The name for this encounter method resource                     | string                     |
| order | A good value for sorting                                        | integer                    |
| names | The name of this encounter method listed in different languages | list [Name](#resourcename) |

## Encounter Conditions
Conditions which affect what pokemon might appear in the wild, e.g., day or night.

### GET api/v2/encounter-condition/{id or name}

###### Example response

```json
{
	"id": 1,
	"name": "swarm",
	"values": [{
		"name": "swarm-yes",
		"url": "http://pokeapi.co/api/v2/encounter-condition-value/1/"
	}, {
		"name": "swarm-no",
		"url": "http://pokeapi.co/api/v2/encounter-condition-value/2/"
	}],
	"names": [{
		"name": "Schwarm",
		"language": {
			"name": "de",
			"url": "http://pokeapi.co/api/v2/language/6/"
		}
	}]
}

```

###### Response models

#### EncounterCondition

| Name   | Description                                                     | Data Type                                                                                           |
|:-------|:----------------------------------------------------------------|:----------------------------------------------------------------------------------------------------|
| id     | The identifier for this encounter condition resource            | integer                                                                                             |
| name   | The name for this encounter condition resource                  | string                                                                                              |
| names  | The name of this encounter method listed in different languages | list [Name](#resourcename)                                                                          |
| values | A list of possible values for this encounter condition          | list [NamedAPIResource](#namedapiresource) ([EncounterConditionValue](#encounter-condition-values)) |

## Encounter Condition Values
Encounter condition values are the various states that an encounter condition can have, i.e., time of day can be either day or night.

### GET api/v2/encounter-condition-value/{id or name}

###### Example response

```json
{
	"id": 1,
	"name": "swarm-yes",
	"condition": {
		"name": "swarm",
		"url": "http://pokeapi.co/api/v2/encounter-condition/1/"
	},
	"names": [{
		"name": "WÃ¤hrend eines Schwarms",
		"language": {
			"name": "de",
			"url": "http://pokeapi.co/api/v2/language/6/"
		}
	}]
}

```

###### Response models

#### EncounterConditionValue

| Name      | Description                                                              | Data Type                                                                                |
|:----------|:-------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------|
| id        | The identifier for this encounter condition value resource               | integer                                                                                  |
| name      | The name for this encounter condition value resource                     | string                                                                                   |
| condition | The condition this encounter condition value pertains to                 | list [NamedAPIResource](#namedapiresource) ([EncounterCondition](#encounter-conditions)) |
| names     | The name of this encounter condition value listed in different languages | list [Name](#resourcename)                                                               |

<h1 id="evolution-section">Evolution</h1>

## Evolution Chains
Evolution chains are essentially family trees. They start with the lowest stage within a family and detail evolution conditions for each as well as Pokémon they can evolve into up through the hierarchy.

### GET api/v2/evolution-chain/{id}

###### Example response

```json
{
	"id": 7,
	"baby_trigger_item": null,
	"chain": {
		"is_baby": false,
		"species": {
			"name": "rattata",
			"url": "http://pokeapi.co/api/v2/pokemon-species/19/"
		},
		"evolution_details": null,
		"evolves_to": [{
			"is_baby": false,
			"species": {
				"name": "raticate",
				"url": "http://pokeapi.co/api/v2/pokemon-species/20/"
			},
			"evolution_details": {
				"item": null,
				"trigger": {
					"name": "level-up",
					"url": "http://pokeapi.co/api/v2/evolution-trigger/1/"
				},
				"gender": null,
				"held_item": null,
				"known_move": null,
				"known_move_type": null,
				"location": null,
				"min_level": 20,
				"min_happiness": null,
				"min_beauty": null,
				"min_affection": null,
				"needs_overworld_rain": false,
				"party_species": null,
				"party_type": null,
				"relative_physical_stats": null,
				"time_of_day": "",
				"trade_species": null,
				"turn_upside_down": false
			},
			"evolves_to": []
		}]
	}
}
```

###### Response models

#### EvolutionChain

| Name              | Description                                                                                                                                                        | Data Type                                              |
|:------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------|
| id                | The identifier for this evolution chain resource                                                                                                                   | integer                                                |
| baby_trigger_item | The item that a Pokémon would be holding when mating that would trigger the egg hatching a baby Pokémon rather than a basic Pokémon                                | [NamedAPIResource](#namedapiresource) ([Item](#items)) |
| chain             | The base chain link object. Each link contains evolution details for a Pokémon in the chain. Each link references the next Pokémon in the natural evolution order. | [ChainLink](#chainlink)                                |

#### ChainLink

| Name              | Description                                                                                    | Data Type                                                                  |
|:------------------|:-----------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------|
| is_baby           | Whether or not this link is for a baby Pokémon. This would only ever be true on the base link. | boolean                                                                    |
| species           | The Pokémon species at this point in the evolution chain                                       | [NamedAPIResource](#namedapiresource) ([PokemonSpecies](#pokemon-species)) |
| evolution_details | All details regarding the specific details of the referenced Pokémon species evolution         | list [EvolutionDetail](#evolutiondetail)                                   |
| evolves_to        | A List of chain objects.                                                                       | list [ChainLink](#chainlink)                                               |

#### EvolutionDetail

| Name                    | Description                                                                                                                                                                 | Data Type                                                                       |
|:------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------|
| item                    | The item required to cause evolution this into Pokémon species                                                                                                              | [NamedAPIResource](#namedapiresource) ([Item](#items))                          |
| trigger                 | The type of event that triggers evolution into this Pokémon species                                                                                                         | [NamedAPIResource](#namedapiresource) ([EvolutionTrigger](#evolution-triggers)) |
| gender                  | The id of the gender of the evolving Pokémon species must be in order to evolve into this Pokémon species                                                                   | integer                                                                         |
| held_item               | The item the evolving Pokémon species must be holding during the evolution trigger event to evolve into this Pokémon species                                                | [NamedAPIResource](#namedapiresource) ([Item](#items))                          |
| known_move              | The move that must be known by the evolving Pokémon species during the evolution trigger event in order to evolve into this Pokémon species                                 | [NamedAPIResource](#namedapiresource) ([Move](#moves))                          |
| known_move_type         | The evolving Pokémon species must know a move with this type during the evolution trigger event in order to evolve into this Pokémon species                                | [NamedAPIResource](#namedapiresource) ([Type](#types))                          |
| location                | The location the evolution must be triggered at.                                                                                                                            | [NamedAPIResource](#namedapiresource) ([Location](#locations))                  |
| min_level               | The minimum required level of the evolving Pokémon species to evolve into this Pokémon species                                                                              | integer                                                                         |
| min_happiness           | The minimum required level of happiness the evolving Pokémon species to evolve into this Pokémon species                                                                    | integer                                                                         |
| min_beauty              | The minimum required level of beauty the evolving Pokémon species to evolve into this Pokémon species                                                                       | integer                                                                         |
| min_affection           | The minimum required level of affection the evolving Pokémon species to evolve into this Pokémon species                                                                    | integer                                                                         |
| needs_overworld_rain    | Whether or not it must be raining in the overworld to cause evolution this Pokémon species                                                                                  | boolean                                                                         |
| party_species           | The Pokémon species that must be in the players party in order for the evolving Pokémon species to evolve into this Pokémon species                                         | [NamedAPIResource](#namedapiresource) ([PokemonSpecies](#pokemon-species))      |
| party_type              | The player must have a Pokémon of this type in their party during the evolution trigger event in order for the evolving Pokémon species to evolve into this Pokémon species | [NamedAPIResource](#namedapiresource) ([Type](#types))                          |
| relative_physical_stats | The required relation between the Pokémon's Attack and Defense stats. 1 means Attack > Defense. 0 means Attack = Defense. -1 means Attack < Defense.                        | integer                                                                         |
| time_of_day             | The required time of day. Day or night.                                                                                                                                     | string                                                                          |
| trade_species           | Pokémon species for which this one must be traded.                                                                                                                          | [NamedAPIResource](#namedapiresource) ([PokemonSpecies](#pokemon-species))      |
| turn_upside_down        | Whether or not the 3DS needs to be turned upside-down as this Pokémon levels up.                                                                                            | boolean                                                                         |

## Evolution Triggers
Evolution triggers are the events and conditions that cause a Pokémon to evolve. Check out [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Methods_of_evolution) for greater detail.

### GET api/v2/evolution-trigger/{id or name}

###### Example response

```json
{
	"id": 1,
	"name": "level-up",
	"names": [{
		"name": "Level up",
		"language": {
			"name": "en",
			"url": "http://pokeapi.co/api/v2/language/9/"
		}
	}],
	"pokemon_species": [{
		"name": "ivysaur",
		"url": "http://pokeapi.co/api/v2/pokemon-species/2/"
	}]
}

```

###### Response models

#### EvolutionTrigger

| Name            | Description                                                       | Data Type                                                                       |
|:----------------|:------------------------------------------------------------------|:--------------------------------------------------------------------------------|
| id              | The identifier for this evolution trigger resource                | integer                                                                         |
| name            | The name for this evolution trigger resource                      | string                                                                          |
| names           | The name of this evolution trigger listed in different languages  | list [Name](#resourcename)                                                      |
| pokemon_species | A list of pokemon species that result from this evolution trigger | list [NamedAPIResource](#namedapiresource) ([PokemonSpecies](#pokemon-species)) |

<h1 id="games-section">Games</h1>

## Generations
A generation is a grouping of the Pokémon games that separates them based on the Pokémon they include. In each generation, a new set of Pokémon, Moves, Abilities and Types that did not exist in the previous generation are released.

### GET api/v2/generation/{id or name}

###### Example response

```json
{
	"id": 1,
	"name": "generation-i",
	"abilities": [],
	"main_region": {
		"name": "kanto",
		"url": "http://pokeapi.co/api/v2/region/1/"
	},
	"moves": [{
		"name": "pound",
		"url": "http://pokeapi.co/api/v2/move/1/"
	}],
	"names": [{
		"name": "Generation I",
		"language": {
			"name": "de",
			"url": "http://pokeapi.co/api/v2/language/6/"
		}
	}],
	"pokemon_species": [{
		"name": "bulbasaur",
		"url": "http://pokeapi.co/api/v2/pokemon-species/1/"
	}],
	"types": [{
		"name": "normal",
		"url": "http://pokeapi.co/api/v2/type/1/"
	}],
	"version_groups": [{
		"name": "red-blue",
		"url": "http://pokeapi.co/api/v2/version-group/1/"
	}]
}

```

###### Response models

#### Generation

| Name            | Description                                                       | Data Type                                                                       |
|:----------------|:------------------------------------------------------------------|:--------------------------------------------------------------------------------|
| id              | The identifier for this generation resource                       | integer                                                                         |
| name            | The name for this generation resource                             | string                                                                          |
| abilities       | A list of abilities that were introduced in this generation       | list [NamedAPIResource](#namedapiresource) ([Ability](#abilities))              |
| names           | The name of this generation listed in different languages         | list [Name](#resourcename)                                                      |
| main_region     | The main region travelled in this generation                      | [NamedAPIResource](#namedapiresource) ([Region](#regions))                      |
| moves           | A list of moves that were introduced in this generation           | list [NamedAPIResource](#namedapiresource) ([Move](#moves))                     |
| pokemon_species | A list of Pokémon species that were introduced in this generation | list [NamedAPIResource](#namedapiresource) ([PokemonSpecies](#pokemon-species)) |
| types           | A list of types that were introduced in this generation           | list [NamedAPIResource](#namedapiresource) ([Type](#types))                     |
| version_groups  | A list of version groups that were introduced in this generation  | list [NamedAPIResource](#namedapiresource) ([VersionGroup](#version-groups))    |

## Pokedexes
A Pokédex is a handheld electronic encyclopedia device; one which is capable of recording and retaining information of the various Pokémon in a given region with the exception of the national dex and some smaller dexes related to portions of a region. See [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Pokedex) for greater detail.

### GET api/v2/pokedex/{id or name}

###### Example response

```json
{
	"id": 2,
	"name": "kanto",
	"is_main_series": true,
	"descriptions": [{
		"description": "Rot/Blau/Gelb Kanto Dex",
		"language": {
			"name": "de",
			"url": "http://pokeapi.co/api/v2/language/6/"
		}
	}],
	"names": [{
		"name": "Kanto",
		"language": {
			"name": "de",
			"url": "http://pokeapi.co/api/v2/language/6/"
		}
	}],
	"pokemon_entries": [{
		"entry_number": 1,
		"pokemon_species": {
			"name": "bulbasaur",
			"url": "http://pokeapi.co/api/v2/pokemon-species/1/"
		}
	}],
	"region": {
		"name": "kanto",
		"url": "http://pokeapi.co/api/v2/region/1/"
	},
	"version_groups": [{
		"name": "red-blue",
		"url": "http://pokeapi.co/api/v2/version-group/1/"
	}]
}
```

###### Response models

#### Pokedex

| Name            | Description                                                                  | Data Type                                                                    |
|:----------------|:-----------------------------------------------------------------------------|:-----------------------------------------------------------------------------|
| id              | The identifier for this Pokédex resource                                     | integer                                                                      |
| name            | The name for this Pokédex resource                                           | string                                                                       |
| is_main_series  | Whether or not this Pokédex originated in the main series of the video games | boolean                                                                      |
| descriptions    | The description of this Pokédex listed in different languages                | list [Description](#description)                                             |
| names           | The name of this Pokédex listed in different languages                       | list [Name](#resourcename)                                                   |
| pokemon_entries | A list of Pokémon catalogued in this Pokédex and their indexes               | list [PokemonEntry](#pokemonentry)                                           |
| region          | The region this Pokédex catalogues Pokémon for                               | [NamedAPIResource](#namedapiresource) ([Region](#regions))                   |
| version_groups  | A list of version groups this Pokédex is relevant to                         | list [NamedAPIResource](#namedapiresource) ([VersionGroup](#version-groups)) |

#### PokemonEntry

| Name            | Description                                                | Data Type                                                                  |
|:----------------|:-----------------------------------------------------------|:---------------------------------------------------------------------------|
| entry_number    | The index of this Pokémon species entry within the Pokédex | integer                                                                    |
| pokemon_species | The Pokémon species being encountered                      | [NamedAPIResource](#namedapiresource) ([PokemonSpecies](#pokemon-species)) |

## Versions
Versions of the games, e.g., Red, Blue or Yellow.

### GET api/v2/version/{id or name}

###### Example response

```json

{
	"id": 1,
	"name": "red",
	"names": [{
		"name": "Rot",
		"language": {
			"name": "de",
			"url": "http://pokeapi.co/api/v2/language/6/"
		}
	}],
	"version_group": {
		"name": "red-blue",
		"url": "http://pokeapi.co/api/v2/version-group/1/"
	}
}
```

###### Response models

#### Version

| Name          | Description                                            | Data Type                                                               |
|:--------------|:-------------------------------------------------------|:------------------------------------------------------------------------|
| id            | The identifier for this version resource               | integer                                                                 |
| name          | The name for this version resource                     | string                                                                  |
| names         | The name of this version listed in different languages | list [Name](#resourcename)                                              |
| version_group | The version group this version belongs to              | [NamedAPIResource](#namedapiresource) ([VersionGroup](#version-groups)) |

## Version Groups
Version groups categorize highly similar versions of the games.

### GET api/v2/version-group/{id or name}

###### example response

```json
{
	"id": 1,
	"name": "red-blue",
	"order": 1,
	"generation": {
		"name": "generation-i",
		"url": "http://pokeapi.co/api/v2/generation/1/"
	},
	"move_learn_methods": [{
		"name": "level-up",
		"url": "http://pokeapi.co/api/v2/move-learn-method/1/"
	}],
	"pokedexes": [{
		"name": "kanto",
		"url": "http://pokeapi.co/api/v2/pokedex/2/"
	}],
	"regions": [{
		"name": "kanto",
		"url": "http://pokeapi.co/api/v2/region/1/"
	}],
	"versions": [{
		"name": "red",
		"url": "http://pokeapi.co/api/v2/version/1/"
	}]
}
```

###### response models

#### VersionGroup

| Name               | Description                                                                                 | Data Type                                                                           |
|:-------------------|:--------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------|
| id                 | The identifier for this version group resource                                              | integer                                                                             |
| name               | The name for this version group resource                                                    | string                                                                              |
| order              | Order for sorting. Almost by date of release, except similar versions are grouped together. | integer                                                                             |
| generation         | The generation this version was introduced in                                               | [NamedAPIResource](#namedapiresource) ([Generation](#generations))                  |
| move_learn_methods | A list of methods in which Pokémon can learn moves in this version group                    | list [NamedAPIResource](#namedapiresource) ([MoveLearnMethod](#move-learn-methods)) |
| pokedexes          | A list of Pokédexes introduces in this version group                                        | list [NamedAPIResource](#namedapiresource) ([Pokedex](#pokedexes))                  |
| regions            | A list of regions that can be visited in this version group                                 | list [NamedAPIResource](#namedapiresource) ([Region](#regions))                     |
| versions           | The versions this version group owns                                                        | list [NamedAPIResource](#namedapiresource) ([Version](#versions))                   |

<h1 id="items-section">Items</h1>

## Items
An item is an object in the games which the player can pick up, keep in their bag, and use in some manner. They have various uses, including healing, powering up, helping catch Pokémon, or to access a new area.

### GET api/v2/item/{id or name}

###### Example response

```json
{
	"id": 1,
	"name": "master-ball",
	"cost": 0,
	"fling_power": 10,
	"fling_effect": {
		"name":"flinch",
		"url":"http://pokeapi.co/api/v2/item-fling-effect/7/"
	},
	"attributes": [{
		"name": "holdable",
		"url": "http://pokeapi.co/api/v2/item-attribute/5/"
	}],
	"category": {
		"name": "standard-balls",
		"url": "http://pokeapi.co/api/v2/item-category/34/"
	},
	"effect_entries": [{
		"effect": "Used in battle\n:   [Catches]{mechanic:catch} a wild Pokémon without fail.\n\n    If used in a trainer battle, nothing happens and the ball is lost.",
		"short_effect": "Catches a wild Pokémon every time.",
		"language": {
			"name": "en",
			"url": "http://pokeapi.co/api/v2/language/9/"
		}
	}],
	"flavor_text_entries": [{
		"text": "The best Poké Ball with the ultimate level of performance. With it, you will catch any wild Pokémon without fail.",
		"version_group": {
			"name": "x-y",
			"url": "http://pokeapi.co/api/v2/version-group/15/"
		},
		"language": {
			"name": "en",
			"url": "http://pokeapi.co/api/v2/language/9/"
		}
	}],
	"game_indices": [{
		"game_index": 1,
		"generation": {
			"name": "generation-vi",
			"url": "http://pokeapi.co/api/v2/generation/6/"
		}
	}],
	"names": [{
		"name": "Master Ball",
		"language": {
			"name": "en",
			"url": "http://pokeapi.co/api/v2/language/9/"
		}
	}],
	"sprites": {
		"default": "http://pokeapi.co/media/sprites/items/master-ball.png"
	},
	"held_by_pokemon": [{
		"pokemon": {
			"name": "chansey",
			"url": "http://pokeapi.co/api/v2/pokemon/113/"
		},
		"version_details": [{
			"rarity": 50,
			"version": {
				"name": "soulsilver",
				"url": "http://pokeapi.co/api/v2/version/16/"
			}
		}]
	}],
	"baby_trigger_for": {
		"url":"http://pokeapi.co/api/v2/evolution-chain/1/"
	}
}
```

###### Response models

#### Item

| Name                | Description                                                          | Data Type                                                                      |
|:--------------------|:---------------------------------------------------------------------|:-------------------------------------------------------------------------------|
| id                  | The identifier for this item resource                                | integer                                                                        |
| name                | The name for this item resource                                      | string                                                                         |
| cost                | The price of this item in stores                                     | integer                                                                        |
| fling_power         | The power of the move Fling when used with this item.                | integer                                                                        |
| fling_effect        | The effect of the move Fling when used with this item                | [NamedAPIResource](#namedapiresource) ([ItemFlingEffect](#item-fling-effects)) |
| attributes          | A list of attributes this item has                                   | list [NamedAPIResource](#namedapiresource) ([ItemAttribute](#item-attributes)) |
| category            | The category of items this item falls into                           | [ItemCategory](#item-categories)                                               |
| effect_entries      | The effect of this ability listed in different languages             | list [VerboseEffect](#verboseeffect)                                           |
| flavor_text_entries | The flavor text of this ability listed in different languages        | list [VersionGroupFlavorText](#versiongroupflavortext)                         |
| game_indices        | A list of game indices relevent to this item by generation           | list [GenerationGameIndex](#generationgameindex)                               |
| names               | The name of this item listed in different languages                  | list [Name](#resourcename)                                                     |
| sprites             | A set of sprites used to depict this item in the game                | [ItemSprites](#item-sprites)                                                   |
| held_by_pokemon     | A list of Pokémon that might be found in the wild holding this item  | list [ItemHolderPokemon](#itemholderpokemon)                                   |
| baby_trigger_for    | An evolution chain this item requires to produce a bay during mating | [APIResource](#apiresource) ([EvolutionChain](#evolution-chains))              |
| machines            | A list of the machines related to this item                          | list [MachineVersionDetail](#machineversiondetail)                     |

#### ItemSprites

| Name    | Description                        | Data Type |
|:--------|:-----------------------------------|:----------|
| default | The default depiction of this item | string    |

#### ItemHolderPokemon

| Name            | Description                                                          | Data Type                                                              |
|:----------------|:---------------------------------------------------------------------|:-----------------------------------------------------------------------|
| pokemon         | The Pokémon that holds this item                                     | string                                                                 |
| version_details | The details for the version that this item is held in by the Pokémon | list [ItemHolderPokemonVersionDetail](#ItemHolderPokemonVersionDetail) |

#### ItemHolderPokemonVersionDetail

| Name    | Description                                            | Data Type                                                   |
|:--------|:-------------------------------------------------------|:------------------------------------------------------------|
| rarity  | How often this Pokémon holds this item in this version | string                                                      |
| version | The version that this item is held in by the Pokémon   | [NamedAPIResource](#namedapiresource) ([Version](#version)) |

## Item Attributes
Item attributes define particular aspects of items, e.g. "usable in battle" or "consumable".

### GET api/v2/item-attribute/{id or name}

###### Example response

```json
{
	"id": 1,
	"name": "countable",
	"descriptions": [{
		"description": "Has a count in the bag",
		"language": {
			"name": "en",
			"url": "http://pokeapi.co/api/v2/language/9/"
		}
	}],
	"items": [{
		"name": "master-ball",
		"url": "http://pokeapi.co/api/v2/item/1/"
	}],
	"names": [{
		"name": "Countable",
		"language": {
			"name": "en",
			"url": "http://pokeapi.co/api/v2/language/9/"
		}
	}]
}
```

###### Response models

#### ItemAttribute

| Name         | Description                                                          | Data Type                                                   |
|:-------------|:---------------------------------------------------------------------|:------------------------------------------------------------|
| id           | The identifier for this item attribute resource                      | integer                                                     |
| name         | The name for this item attribute resource                            | string                                                      |
| items        | A list of items that have this attribute                             | list [NamedAPIResource](#namedapiresource) ([Item](#items)) |
| names        | The name of this item attribute listed in different languages        | list [Name](#resourcename)                                  |
| descriptions | The description of this item attribute listed in different languages | list [Description](#description)                            |

## Item Categories
Item categories determine where items will be placed in the players bag.

### GET api/v2/item-category/{id or name}

###### example response

```json
{
	"id": 1,
	"name": "stat-boosts",
	"items": [{
		"name": "guard-spec",
		"url": "http://pokeapi.co/api/v2/item/55/"
	}],
	"names": [{
		"name": "Stat boosts",
		"language": {
			"name": "en",
			"url": "http://pokeapi.co/api/v2/language/9/"
		}
	}],
	"pocket": {
		"name": "battle",
		"url": "http://pokeapi.co/api/v2/item-pocket/7/"
	}
}
```

###### response models

#### ItemCategory

| Name   | Description                                                  | Data Type                                                           |
|:-------|:-------------------------------------------------------------|:--------------------------------------------------------------------|
| id     | The identifier for this item category resource               | integer                                                             |
| name   | The name for this item category resource                     | string                                                              |
| items  | A list of items that are a part of this category             | list [NamedAPIResource](#namedapiresource) ([Item](#items))         |
| names  | The name of this item category listed in different languages | list [Name](#resourcename)                                          |
| pocket | The pocket items in this category would be put in            | [NamedAPIResource](#namedapiresource) ([ItemPocket](#item-pockets)) |

## Item Fling Effects
The various effects of the move "Fling" when used with different items.

### GET api/v2/item-fling-effect/{id or name}

###### example response

```json
{
	"id": 1,
	"name": "badly-poison",
	"effect_entries": [{
		"effect": "Badly poisons the target.",
		"language": {
			"name": "en",
			"url": "http://pokeapi.co/api/v2/language/9/"
		}
	}],
	"items": [{
		"name": "toxic-orb",
		"url": "http://pokeapi.co/api/v2/item/249/"
	}]
}
```

###### response models

#### ItemFlingEffect

| Name           | Description                                                   | Data Type                                                   |
|:---------------|:--------------------------------------------------------------|:------------------------------------------------------------|
| id             | The identifier for this fling effect resource                 | integer                                                     |
| name           | The name for this fling effect resource                       | string                                                      |
| effect_entries | The result of this fling effect listed in different languages | list [Effect](#effect)                                      |
| items          | A list of items that have this fling effect                   | list [NamedAPIResource](#namedapiresource) ([Item](#items)) |

## Item Pockets
Pockets within the players bag used for storing items by category.

### GET api/v2/item-pocket/{id or name}

###### Example response

```json
{
	"id": 1,
	"name": "misc",
	"categories": [{
		"name": "collectibles",
		"url": "http://pokeapi.co/api/v2/item-category/9/"
	}],
	"names": [{
		"name": "Items",
		"language": {
			"name": "en",
			"url": "http://pokeapi.co/api/v2/language/9/"
		}
	}]
}
```

###### Response models

#### ItemPocket

| Name       | Description                                                     | Data Type                                                                     |
|:-----------|:----------------------------------------------------------------|:------------------------------------------------------------------------------|
| id         | The identifier for this item pocket resource                    | integer                                                                       |
| name       | The name for this item pocket resource                          | string                                                                        |
| categories | A list of item categories that are relevant to this item pocket | list [NamedAPIResource](#namedapiresource) ([ItemCategory](#item-categories)) |
| names      | The name of this item pocket listed in different languages      | list [Name](#resourcename)                                                    |

<h1 id="machines-section">Machines</h1>

## Machines
Machines are the representation of items that teach moves to Pokémon. They vary from version to version, so it is not certain that one specific TM or HM corresponds to a single Machine.

### GET api/v2/machine/{id}

###### Example response

```json
{
    "id": 1,
    "item": {
        "name": "tm01",
        "url": "http://localhost:8000/api/v2/item/305/"
    },
    "move": {
        "name": "mega-punch",
        "url": "http://localhost:8000/api/v2/move/5/"
    },
    "version_group": {
        "name": "red-blue",
        "url": "http://localhost:8000/api/v2/version/1/"
    }
}
```

###### Response models

#### Machine

| Name          | Description                                        | Data Type                                                               |
|:--------------|:---------------------------------------------------|:------------------------------------------------------------------------|
| id            | The identifier for this machine resource           | integer                                                                 |
| item          | The TM or HM item that corresponds to this machine | [NamedAPIResource](#namedapiresource) ([Item](#items))                  |
| move          | The move that is taught by this machine            | [NamedAPIResource](#namedapiresource) ([Move](#moves))                  |
| version_group | The version group that this machine applies to     | [NamedAPIResource](#namedapiresource) ([VersionGroup](#version-groups)) |

<h1 id="moves-section">Moves</h1>

## Moves
Moves are the skills of Pokémon in battle. In battle, a Pokémon uses one move each turn. Some moves (including those learned by Hidden Machine) can be used outside of battle as well, usually for the purpose of removing obstacles or exploring new areas.

### GET api/v2/move/{id or name}

###### Example response

```json
{
	"id": 1,
	"name": "pound",
	"accuracy": 100,
	"effect_chance": null,
	"pp": 35,
	"priority": 0,
	"power": 40,
	"contest_combos": {
		"normal": {
			"use_before": [{
				"name": "double-slap",
				"url": "http://pokeapi.co/api/v2/move/3/"
			}, {
				"name": "headbutt",
				"url": "http://pokeapi.co/api/v2/move/29/"
			}, {
				"name": "feint-attack",
				"url": "http://pokeapi.co/api/v2/move/185/"
			}],
			"use_after": null
		},
		"super": {
			"use_before": null,
			"use_after": null
		}
	},
	"contest_type": {
		"name": "tough",
		"url": "http://pokeapi.co/api/v2/contest-type/5/"
	},
	"contest_effect": {
		"url": "http://pokeapi.co/api/v2/contest-effect/1/"
	},
	"damage_class": {
		"name": "physical",
		"url": "http://pokeapi.co/api/v2/move-damage-class/2/"
	},
	"effect_entries": [{
		"effect": "Inflicts [regular damage]{mechanic:regular-damage}.",
		"short_effect": "Inflicts regular damage with no additional effect.",
		"language": {
			"name": "en",
			"url": "http://pokeapi.co/api/v2/language/9/"
		}
	}],
	"effect_changes": [],
	"generation": {
		"name": "generation-i",
		"url": "http://pokeapi.co/api/v2/generation/1/"
	},
	"meta": {
		"ailment": {
			"name": "none",
			"url": "http://pokeapi.co/api/v2/move-ailment/0/"
		},
		"category": {
			"name": "damage",
			"url": "http://pokeapi.co/api/v2/move-category/0/"
		},
		"min_hits": null,
		"max_hits": null,
		"min_turns": null,
		"max_turns": null,
		"drain": 0,
		"healing": 0,
		"crit_rate": 0,
		"ailment_chance": 0,
		"flinch_chance": 0,
		"stat_chance": 0
	},
	"names": [{
		"name": "Pound",
		"language": {
			"name": "en",
			"url": "http://pokeapi.co/api/v2/language/9/"
		}
	}],
	"past_values": [],
	"stat_changes": [],
	"super_contest_effect": {
		"url": "http://pokeapi.co/api/v2/super-contest-effect/5/"
	},
	"target": {
		"name": "selected-pokemon",
		"url": "http://pokeapi.co/api/v2/move-target/10/"
	},
	"type": {
		"name": "normal",
		"url": "http://pokeapi.co/api/v2/type/1/"
	},
  "flavor_text_entries": [
		{
			"flavor_text": "Pounds with fore­\nlegs or tail.",
			"language": {
				"url": "http://localhost:8000/api/v2/language/9/",
				"name": "en"
			},
			"version_group": {
				"url": "http://localhost:8000/api/v2/version-group/3/",
				"name": "gold-silver"
			}
		},
  }]
}
```

###### Response models

#### Move

| Name                 | Description                                                                                                                                                               | Data Type                                                                       |
|:---------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------|
| id                   | The identifier for this move resource                                                                                                                                     | integer                                                                         |
| name                 | The name for this move resource                                                                                                                                           | string                                                                          |
| accuracy             | The percent value of how likely this move is to be successful                                                                                                             | integer                                                                         |
| effect_chance        | The percent value of how likely it is this moves effect will happen                                                                                                       | integer                                                                         |
| pp                   | Power points. The number of times this move can be used                                                                                                                   | integer                                                                         |
| priority             | A value between -8 and 8. Sets the order in which moves are executed during battle. See [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Priority) for greater detail. | integer                                                                         |
| power                | The base power of this move with a value of 0 if it does not have a base power                                                                                            | integer                                                                         |
| contest_combos       | A detail of normal and super contest combos that require this move                                                                                                        | [ContestComboSets](#contestcombosets)                                           |
| contest_type         | The type of appeal this move gives a Pokémon when used in a contest                                                                                                       | [NamedAPIResource](#namedapiresource) ([ContestType](#contest-types))           |
| contest_effect       | The effect the move has when used in a contest                                                                                                                            | [APIResource](#apiresource) ([ContestEffect](#contest-effects))                 |
| damage_class         | The type of damage the move inflicts on the target, e.g. physical                                                                                                         | [NamedAPIResource](#namedapiresource) ([MoveDamageClass](#move-damage-classes)) |
| effect_entries       | The effect of this move listed in different languages                                                                                                                     | list [VerboseEffect](#verboseeffect)                                            |
| effect_changes       | The list of previous effects this move has had across version groups of the games                                                                                         | list [AbilityEffectChange](#abilityeffectchange)                                |
| flavor_text_entries  | The flavor text of this move listed in different languages                                                                                                                | list [MoveFlavorText](#moveflavortext)                                                         |
| generation           | The generation in which this move was introduced                                                                                                                          | [NamedAPIResource](#namedapiresource) ([Generation](#generations))              |
| machines             | A list of the machines that teach this move                                                                                                                               | list [MachineVersionDetail](#machineversiondetail)                              |
| meta                 | Metadata about this move                                                                                                                                                  | [MoveMetaData](#movemetadata)                                                   |
| names                | The name of this move listed in different languages                                                                                                                       | list [Name](#resourcename)                                                      |
| past_values          | A list of move resource value changes across version groups of the game                                                                                                   | list [PastMoveStatValues](#pastmovestatvalues)                                  |
| stat_changes         | A list of stats this moves effects and how much it effects them                                                                                                           | list [MoveStatChange](#movestatchange)                                          |
| super_contest_effect | The effect the move has when used in a super contest                                                                                                                      | [APIResource](#apiresource) ([SuperContestEffect](#super-contest-effects))      |
| target               | The type of target that will receive the effects of the attack                                                                                                            | [NamedAPIResource](#namedapiresource) ([MoveTarget](#move-targets))             |
| type                 | The elemental type of this move                                                                                                                                           | [NamedAPIResource](#namedapiresource) ([Type](#types))                          |

#### ContestComboSets

| Name   | Description                                                                                                  | Data Type                                 |
|:-------|:-------------------------------------------------------------------------------------------------------------|:------------------------------------------|
| normal | A detail of moves this move can be used before or after, granting additional appeal points in contests       | [ContestComboDetail](#contestcombodetail) |
| super  | A detail of moves this move can be used before or after, granting additional appeal points in super contests | [ContestComboDetail](#contestcombodetail) |

#### ContestComboDetail

| Name       | Description                             | Data Type                                                   |
|:-----------|:----------------------------------------|:------------------------------------------------------------|
| use_before | A list of moves to use before this move | list [NamedAPIResource](#namedapiresource) ([Move](#moves)) |
| use_after  | A list of moves to use after this move  | list [NamedAPIResource](#namedapiresource) ([Move](#moves)) |

#### MoveFlavorText

| Name          | Description                                                          | Data Type                                                               |
|:--------------|:---------------------------------------------------------------------|:------------------------------------------------------------------------|
| flavor_text   | The localized flavor text for an api resource in a specific language | string                                                                  |
| language      | The language this name is in                                  		   | [NamedAPIResource](#namedapiresource) ([Language](#languages))          |
| version_group | The version group that uses this flavor text                         | [NamedAPIResource](#namedapiresource) ([VersionGroup](#version-groups)) |

#### MoveMetaData

| Name           | Description                                                                                            | Data Type                                                             |
|:---------------|:-------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------|
| ailment        | The status ailment this move inflicts on its target                                                    | [NamedAPIResource](#namedapiresource) ([MoveAilment](#move-ailments)) |
| category       | The category of move this move falls under, e.g. damage or ailment                                     | [NamedAPIResource](#namedapiresource) ([Move](#moves))                |
| min_hits       | The minimum number of times this move hits. Null if it always only hits once.                          | integer                                                               |
| max_hits       | The maximum number of times this move hits. Null if it always only hits once.                          | integer                                                               |
| min_turns      | The minimum number of turns this move continues to take effect. Null if it always only lasts one turn. | integer                                                               |
| max_turns      | The maximum number of turns this move continues to take effect. Null if it always only lasts one turn. | integer                                                               |
| drain          | HP drain (if positive) or Recoil damage (if negative), in percent of damage done                       | integer                                                               |
| healing        | The amount of hp gained by the attacking Pokemon, in percent of it's maximum HP                        | integer                                                               |
| crit_rate      | Critical hit rate bonus                                                                                | integer                                                               |
| ailment_chance | The likelihood this attack will cause an ailment                                                       | integer                                                               |
| flinch_chance  | The likelihood this attack will cause the target Pokémon to flinch                                     | integer                                                               |
| stat_chance    | The likelihood this attack will cause a stat change in the target Pokémon                              | integer                                                               |

#### MoveStatChange

| Name   | Description             | Data Type                                              |
|:-------|:------------------------|:-------------------------------------------------------|
| change | The amount of change    | integer                                                |
| stat   | The stat being affected | [NamedAPIResource](#namedapiresource) ([Stat](#stats)) |

#### PastMoveStatValues

| Name           | Description                                                                    | Data Type                                                               |
|:---------------|:-------------------------------------------------------------------------------|:------------------------------------------------------------------------|
| accuracy       | The percent value of how likely this move is to be successful                  | integer                                                                 |
| effect_chance  | The percent value of how likely it is this moves effect will take effect       | integer                                                                 |
| power          | The base power of this move with a value of 0 if it does not have a base power | integer                                                                 |
| pp             | Power points. The number of times this move can be used                        | integer                                                                 |
| effect_entries | The effect of this move listed in different languages                          | list [VerboseEffect](#verboseeffect)                                    |
| type           | The elemental type of this move                                                | [NamedAPIResource](#namedapiresource) ([Type](#types))                  |
| version_group  | The version group in which these move stat values were in effect               | [NamedAPIResource](#namedapiresource) ([VersionGroup](#version-groups)) |

## Move Ailments
Move Ailments are status conditions caused by moves used during battle. See [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/http://bulbapedia.bulbagarden.net/wiki/Status_condition) for greater detail.

### GET api/v2/move-ailment/{id or name}

###### Example response

```json
{
	"id": 1,
	"name": "paralysis",
	"moves": [{
		"name": "thunder-punch",
		"url": "http://pokeapi.co/api/v2/move/9/"
	}],
	"names": [{
		"name": "Paralysis",
		"language": {
			"name": "en",
			"url": "http://pokeapi.co/api/v2/language/9/"
		}
	}]
}
```

###### Response models

#### Move Ailment

| Name  | Description                                                 | Data Type                                                   |
|:------|:------------------------------------------------------------|:------------------------------------------------------------|
| id    | The identifier for this move ailment resource               | integer                                                     |
| name  | The name for this move ailment resource                     | string                                                      |
| moves | A list of moves that cause this ailment                     | list [NamedAPIResource](#namedapiresource) ([Move](#moves)) |
| names | The name of this move ailment listed in different languages | list [Name](#resourcename)                                  |

## Move Battle Styles
Styles of moves when used in the Battle Palace. See [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Battle_Frontier_(Generation_III)) for greater detail.

### GET api/v2/move-battle-style/{id or name}

###### Example response

```json
{
	"id": 1,
	"name": "attack",
	"names": [{
		"name": "Attack",
		"language": {
			"name": "en",
			"url": "http://pokeapi.co/api/v2/language/9/"
		}
	}]
}
```

###### Response models

#### Move Battle Style

| Name  | Description                                                      | Data Type                  |
|:------|:-----------------------------------------------------------------|:---------------------------|
| id    | The identifier for this move battle style resource               | integer                    |
| name  | The name for this move battle style resource                     | string                     |
| names | The name of this move battle style listed in different languages | list [Name](#resourcename) |

## Move Categories
Very general categories that loosely group move effects.

### GET api/v2/move-category/{id or name}

###### Example response

```json
{
	"id": 1,
	"name": "ailment",
	"descriptions": [{
		"description": "No damage; inflicts status ailment",
		"language": {
			"name": "en",
			"url": "http://pokeapi.co/api/v2/language/9/"
		}
	}],
	"moves": [{
		"name": "sing",
		"url": "http://pokeapi.co/api/v2/move/47/"
	}]
}
```

###### Response models

#### Move Category

| Name         | Description                                                        | Data Type                                                   |
|:-------------|:-------------------------------------------------------------------|:------------------------------------------------------------|
| id           | The identifier for this move category resource                     | integer                                                     |
| name         | The name for this move category resource                           | string                                                      |
| moves        | A list of moves that fall into this category                       | list [NamedAPIResource](#namedapiresource) ([Move](#moves)) |
| descriptions | The description of this move ailment listed in different languages | list [Description](#description)                            |

## Move Damage Classes
Damage classes moves can have, e.g. physical, special, or non-damaging.

### GET api/v2/move-damage-class/{id or name}

###### Example response

```json
{
	"id": 1,
	"name": "status",
	"descriptions": [{
		"description": "ãƒ€ãƒ¡ãƒ¼ã‚¸ãªã„",
		"language": {
			"name": "ja",
			"url": "http://pokeapi.co/api/v2/language/1/"
		}
	}],
	"moves": [{
		"name": "swords-dance",
		"url": "http://pokeapi.co/api/v2/move/14/"
	}]
}
```

###### Response models

#### Move Damage Class

| Name         | Description                                                             | Data Type                                                   |
|:-------------|:------------------------------------------------------------------------|:------------------------------------------------------------|
| id           | The identifier for this move damage class resource                      | integer                                                     |
| name         | The name for this move damage class resource                            | string                                                      |
| descriptions | The description of this move damage class listed in different languages | list [Description](#description)                            |
| moves        | A list of moves that fall into this damage class                        | list [NamedAPIResource](#namedapiresource) ([Move](#moves)) |
| names        | The name of this move damage class listed in different languages        | list [Name](#resourcename)                                  |

## Move Learn Methods
Methods by which Pokémon can learn moves.

### GET api/v2/move-learn-method/{id or name}

###### Example response

```json
{
	"id": 1,
	"name": "level-up",
	"names": [{
		"name": "Level up",
		"language": {
			"name": "de",
			"url": "http://pokeapi.co/api/v2/language/6/"
		}
	}],
	"descriptions": [{
		"description": "Wird gelernt, wenn ein Pokémon ein bestimmtes Level erreicht.",
		"language": {
			"name": "de",
			"url": "http://pokeapi.co/api/v2/language/6/"
		}
	}],
	"version_groups": [{
		"name": "red-blue",
		"url": "http://pokeapi.co/api/v2/version-group/1/"
	}]
}
```

###### Response models

#### Move Learn Method

| Name           | Description                                                             | Data Type                                                                    |
|:---------------|:------------------------------------------------------------------------|:-----------------------------------------------------------------------------|
| id             | The identifier for this move learn method resource                      | integer                                                                      |
| name           | The name for this move learn method resource                            | string                                                                       |
| descriptions   | The description of this move learn method listed in different languages | list [Description](#description)                                             |
| names          | The name of this move learn method listed in different languages        | list [Name](#resourcename)                                                   |
| version_groups | A list of version groups where moves can be learned through this method | list [NamedAPIResource](#namedapiresource) ([VersionGroup](#version-groups)) |

## Move Targets
Targets moves can be directed at during battle. Targets can be Pokémon, environments or even other moves.

### GET api/v2/move-target/{id or name}

###### Example response

```json
{
	"id": 1,
	"name": "specific-move",
	"descriptions": [{
		"description": "Eine spezifische Fähigkeit. Wie diese Fähigkeit genutzt wird, hängt von den genutzten Fähigkeiten ab.",
		"language": {
			"name": "de",
			"url": "http://pokeapi.co/api/v2/language/6/"
		}
	}],
	"moves": [{
		"name": "counter",
		"url": "http://pokeapi.co/api/v2/move/68/"
	}],
	"names": [{
		"name": "Spezifische Fähigkeit",
		"language": {
			"name": "de",
			"url": "http://pokeapi.co/api/v2/language/6/"
		}
	}]
}
```

###### Response models

#### Move Target

| Name         | Description                                                       | Data Type                                                   |
|:-------------|:------------------------------------------------------------------|:------------------------------------------------------------|
| id           | The identifier for this move target resource                      | integer                                                     |
| name         | The name for this move target resource                            | string                                                      |
| descriptions | The description of this move target listed in different languages | list [Description](#description)                            |
| moves        | A list of moves that that are directed at this target             | list [NamedAPIResource](#namedapiresource) ([Move](#moves)) |
| names        | The name of this move target listed in different languages        | list [Name](#resourcename)                                  |

<h1 id="locations-section">Locations</h1>

## Locations
Locations that can be visited within the games. Locations make up sizable portions of regions, like cities or routes.

### GET api/v2/location/{id}

###### Example response

```json
{
	"id": 1,
	"name": "canalave-city",
	"region": {
		"name": "sinnoh",
		"url": "http://pokeapi.co/api/v2/region/4/"
	},
	"names": [{
		"name": "Canalave City",
		"language": {
			"name": "en",
			"url": "http://pokeapi.co/api/v2/language/9/"
		}
	}],
	"game_indices": [{
		"game_index": 7,
		"generation": {
			"name": "generation-iv",
			"url": "http://pokeapi.co/api/v2/generation/4/"
		}
	}],
	"areas": [{
		"name": "canalave-city-area",
		"url": "http://pokeapi.co/api/v2/location-area/1/"
	}]
}
```

###### Response models

#### Location

| Name         | Description                                                    | Data Type                                                                    |
|:-------------|:---------------------------------------------------------------|:-----------------------------------------------------------------------------|
| id           | The identifier for this location resource                      | integer                                                                      |
| name         | The name for this location resource                            | string                                                                       |
| region       | The region this location can be found in                       | [NamedAPIResource](#namedapiresource) ([Region](#regions))                   |
| names        | The name of this language listed in different languages        | list [Name](#resourcename)                                                   |
| game_indices | A list of game indices relevent to this location by generation | list [GenerationGameIndex](#generationgameindex)                             |
| areas        | Areas that can be found within this location                   | list [NamedAPIResource](#namedapiresource) ([LocationArea](#location-areas)) |

## Location Areas
Location areas are sections of areas, such as floors in a building or cave. Each area has its own set of possible Pokémon encounters.

### GET api/v2/location-area/{id}

###### Example response

```json
{
	"id": 1,
	"name": "canalave-city-area",
	"game_index": 1,
	"encounter_method_rates": [{
		"encounter_method": {
			"name": "old-rod",
			"url": "http://pokeapi.co/api/v2/encounter-method/2/"
		},
		"version_details": [{
			"rate": 25,
			"version": {
				"name": "platinum",
				"url": "http://pokeapi.co/api/v2/version/14/"
			}
		}]
	}],
	"location": {
		"name": "canalave-city",
		"url": "http://pokeapi.co/api/v2/location/1/"
	},
	"names": [{
		"name": "",
		"language": {
			"name": "en",
			"url": "http://pokeapi.co/api/v2/language/9/"
		}
	}],
	"pokemon_encounters": [{
		"pokemon": {
			"name": "tentacool",
			"url": "http://pokeapi.co/api/v2/pokemon/72/"
		},
		"version_details": [{
			"version": {
				"name": "diamond",
				"url": "http://pokeapi.co/api/v2/version/12/"
			},
			"max_chance": 60,
			"encounter_details": [{
				"min_level": 20,
				"max_level": 30,
				"condition_values": [],
				"chance": 60,
				"method": {
					"name": "surf",
					"url": "http://pokeapi.co/api/v2/encounter-method/5/"
				}
			}]
		}]
	}]
}
```

###### Response models

#### LocationArea

| Name                   | Description                                                                                                                                  | Data Type                                                  |
|:-----------------------|:---------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------|
| id                     | The identifier for this location resource                                                                                                    | integer                                                    |
| name                   | The name for this location resource                                                                                                          | string                                                     |
| game_index             | The internal id of an API resource within game data                                                                                          | integer                                                    |
| encounter_method_rates | A list of methods in which Pokémon may be encountered in this area and how likely the method will occur depending on the version of the game | list [EncounterMethodRate](#encountermethodrate)           |
| location               | The region this location can be found in                                                                                                     | [NamedAPIResource](#namedapiresource) ([Region](#regions)) |
| names                  | The name of this location area listed in different languages                                                                                 | list [Name](#resourcename)                                 |
| pokemon_encounters     | A list of Pokémon that can be encountered in this area along with version specific details about the encounter                               | list [PokemonEncounter](#pokemonencounter)                 |

#### EncounterMethodRate

| Name             | Description                                                    | Data Type                                                                   |
|:-----------------|:---------------------------------------------------------------|:----------------------------------------------------------------------------|
| encounter_method | The method in which Pokémon may be encountered in an area.     | [NamedAPIResource](#namedapiresource) ([EncounterMethod](#encountermehtod)) |
| version_details  | The chance of the encounter to occur on a version of the game. | list [EncounterVersionDetails](#encounterversiondetails)                    |

#### EncounterVersionDetails

| Name    | Description                                                                     | Data Type                                                   |
|:--------|:--------------------------------------------------------------------------------|:------------------------------------------------------------|
| rate    | The chance of an encounter to occur.                                            | integer                                                     |
| version | The version of the game in which the encounter can occur with the given chance. | [NamedAPIResource](#namedapiresource) ([Version](#version)) |

#### PokemonEncounter

| Name            | Description                                                                                      | Data Type                                                   |
|:----------------|:-------------------------------------------------------------------------------------------------|:------------------------------------------------------------|
| pokemon         | The Pokémon being encountered                                                                    | [NamedAPIResource](#namedapiresource) ([Pokemon](#pokemon)) |
| version_details | A list of versions and encounters with Pokémon that might happen in the referenced location area | list [VersionEncounterDetail](#versionencounterdetail)      |

## Pal Park Areas
Areas used for grouping Pokémon encounters in Pal Park. They're like habitats that are specific to Pal Park.

### GET api/v2/pal-park-area/{id or name}

###### Example response

```json
{
	"id": 1,
	"name": "forest",
	"names": [{
		"name": "Forest",
		"language": {
			"name": "en",
			"url": "http://pokeapi.co/api/v2/language/9/"
		}
	}],
	"pokemon_encounters": [{
		"base_score": 30,
		"rate": 50,
		"pokemon_species": {
			"name": "caterpie",
			"url": "http://pokeapi.co/api/v2/pokemon-species/10/"
		}
	}]
}
```

###### Response models

#### PalParkArea

| Name               | Description                                                           | Data Type                                                |
|:-------------------|:----------------------------------------------------------------------|:---------------------------------------------------------|
| id                 | The identifier for this pal park area resource                        | integer                                                  |
| name               | The name for this pal park area resource                              | string                                                   |
| names              | The name of this pal park area listed in different languages          | list [Name](#resourcename)                               |
| pokemon_encounters | A list of Pokémon encountered in thi pal park area along with details | list [PalParkEncounterSpecies](#palparkencounterspecies) |

#### PalParkEncounterSpecies

| Name            | Description                                                                          | Data Type                                                                 |
|:----------------|:-------------------------------------------------------------------------------------|:--------------------------------------------------------------------------|
| base_score      | The base score given to the player when this Pokémon is caught during a pal park run | integer                                                                   |
| rate            | The base rate for encountering this Pokémon in this pal park area                    | integer                                                                   |
| pokemon_species | The Pokémon species being encountered                                                | [NamedAPIResource](#namedapiresource) ([PokemonSpecies](#pokemonspecies)) |

## Regions
A region is an organized area of the Pokémon world. Most often, the main difference between regions is the species of Pokémon that can be encountered within them.

### GET api/v2/region/{id or name}

###### Example response

```json
{
	"id": 1,
	"name": "kanto",
	"locations": [{
		"name": "celadon-city",
		"url": "http://pokeapi.co/api/v2/location/67/"
	}],
	"main_generation": {
		"name": "generation-i",
		"url": "http://pokeapi.co/api/v2/generation/1/"
	},
	"names": [{
		"name": "Kanto",
		"language": {
			"name": "de",
			"url": "http://pokeapi.co/api/v2/language/6/"
		}
	}],
	"pokedexes": [{
		"name": "kanto",
		"url": "http://pokeapi.co/api/v2/pokedex/2/"
	}],
	"version_groups": [{
		"name": "red-blue",
		"url": "http://pokeapi.co/api/v2/version-group/1/"
	}]
}
```

###### Response models

#### Region

| Name            | Description                                               | Data Type                                                                    |
|:----------------|:----------------------------------------------------------|:-----------------------------------------------------------------------------|
| id              | The identifier for this region resource                   | integer                                                                      |
| name            | The name for this region resource                         | string                                                                       |
| locations       | A list of locations that can be found in this region      | list [NamedAPIResource](#namedapiresource) ([Location](#locations))          |
| main_generation | The generation this region was introduced in              | [NamedAPIResource](#namedapiresource) ([Generation](#generations))           |
| names           | The name of this region listed in different languages     | list [Name](#resourcename)                                                   |
| pokedexes       | A list of pokédexes that catalogue Pokémon in this region | list [NamedAPIResource](#namedapiresource) ([Pokedex](#pokedexes))           |
| version_groups  | A list of version groups where this region can be visited | list [NamedAPIResource](#namedapiresource) ([VersionGroup](#version-groups)) |

<h1 id="pokemon-section">Pokemon</h1>

## Abilities

Abilities provide passive effects for Pokémon in battle or in the overworld. Pokémon have multiple possible abilities but can have only one ability at a time. Check out [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Ability) for greater detail.

### GET api/v2/ability/{id or name}

###### Example response

```json
{
	"id": 1,
	"name": "stench",
	"is_main_series": true,
	"generation": {
		"name": "generation-iii",
		"url": "http://pokeapi.co/api/v2/generation/3/"
	},
	"names": [{
		"name": "Stench",
		"language": {
			"name": "en",
			"url": "http://pokeapi.co/api/v2/language/9/"
		}
	}],
	"effect_entries": [{
		"effect": "This Pokémon's damaging moves have a 10% chance to make the target [flinch]{mechanic:flinch} with each hit if they do not already cause flinching as a secondary effect.\n\nThis ability does not stack with a held item.\n\nOverworld: The wild encounter rate is halved while this Pokémon is first in the party.",
		"short_effect": "Has a 10% chance of making target Pokémon [flinch]{mechanic:flinch} with each hit.",
		"language": {
			"name": "en",
			"url": "http://pokeapi.co/api/v2/language/9/"
		}
	}],
	"effect_changes": [{
		"version_group": {
			"name": "black-white",
			"url": "http://pokeapi.co/api/v2/version-group/11/"
		},
		"effect_entries": [{
			"effect": "Has no effect in battle.",
			"language": {
				"name": "en",
				"url": "http://pokeapi.co/api/v2/language/9/"
			}
		}]
	}],
	"flavor_text_entries": [{
		"flavor_text": "è‡­ãã¦ã€€ç›¸æ‰‹ãŒ\nã²ã‚‹ã‚€ã€€ã“ã¨ãŒã‚ã‚‹ã€‚",
		"language": {
			"name": "ja-kanji",
			"url": "http://pokeapi.co/api/v2/language/11/"
		},
		"version_group": {
			"name": "x-y",
			"url": "http://pokeapi.co/api/v2/version-group/15/"
		}
	}],
	"pokemon": [{
		"is_hidden": true,
		"slot": 3,
		"pokemon": {
			"name": "gloom",
			"url": "http://pokeapi.co/api/v2/pokemon/44/"
		}
	}]
}
```

###### Response models

#### Ability

| Name                | Description                                                                  | Data Type                                                          |
|:--------------------|:-----------------------------------------------------------------------------|:-------------------------------------------------------------------|
| id                  | The identifier for this ability resource                                     | integer                                                            |
| name                | The name for this ability resource                                           | string                                                             |
| is_main_series      | Whether or not this ability originated in the main series of the video games | boolean                                                            |
| generation          | The generation this ability originated in                                    | [NamedAPIResource](#namedapiresource) ([Generation](#generations)) |
| names               | The name of this ability listed in different languages                       | list [Name](#resourcename)                                         |
| effect_entries      | The effect of this ability listed in different languages                     | list [VerboseEffect](#verboseeffect)                               |
| effect_changes      | The list of previous effects this ability has had across version groups      | list [AbilityEffectChange](#abilityeffectchange)                   |
| flavor_text_entries | The flavor text of this ability listed in different languages                | list [AbilityFlavorText](#abilityflavortext)                       |
| pokemon             | A list of Pokémon that could potentially have this ability                   | list [AbilityPokemon](#abilitypokemon)                             |

#### AbilityEffectChange

| Name           | Description                                                               | Data Type                                                              |
|:---------------|:--------------------------------------------------------------------------|:-----------------------------------------------------------------------|
| effect_entries | The previous effect of this ability listed in different languages         | list [Effect](#effect)                                                 |
| version_group  | The version group in which the previous effect of this ability originated | [NamedAPIResource](#namedapiresource) ([VersionGroup](#versiongroups)) |

#### AbilityFlavorText

| Name          | Description                                                   | Data Type                                                               |
|:--------------|:--------------------------------------------------------------|:------------------------------------------------------------------------|
| flavor_text   | The localized name for an API resource in a specific language | string                                                                  |
| language      | The language this name is in                                  | [NamedAPIResource](#namedapiresource) ([Language](#languages))          |
| version_group | The version group that uses this flavor text                  | [NamedAPIResource](#namedapiresource) ([VersionGroup](#version-groups)) |

#### AbilityPokemon

| Name      | Description                                                                                                                                              | Data Type                                                   |
|:----------|:---------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------|
| is_hidden | Whether or not this a hidden ability for the referenced Pokémon                                                                                          | boolean                                                     |
| slot      | Pokémon have 3 ability 'slots' which hold references to possible abilities they could have. This is the slot of this ability for the referenced pokemon. | integer                                                     |
| pokemon   | The Pokémon this ability could belong to                                                                                                                 | [NamedAPIResource](#namedapiresource) ([Pokemon](#pokemon)) |

## Characteristics
Characteristics indicate which stat contains a Pokémon's highest IV. A Pokémon's Characteristic is determined by the remainder of its highest IV divided by 5 (gene_modulo). Check out [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Characteristic) for greater detail.

### GET api/v2/characteristic/{id}

###### Example response

```json
{
	"id": 1,
	"gene_modulo": 0,
	"possible_values": [0, 5, 10, 15, 20, 25, 30],
	"highest_stat": {
		"name": "hp",
		"url": "http://pokeapi.co/api/v2/stat/1/"
	},
	"descriptions": [{
		"description": "Loves to eat",
		"language": {
			"name": "en",
			"url": "http://pokeapi.co/api/v2/language/9/"
		}
	}]
}

```

###### Response models

#### Characteristic

| Name            | Description                                                                                                            | Data Type                          |
|:----------------|:-----------------------------------------------------------------------------------------------------------------------|:-----------------------------------|
| id              | The identifier for this characteristic resource                                                                        | integer                            |
| gene_modulo     | The remainder of the highest stat/IV divided by 5                                                                      | integer                            |
| possible_values | The possible values of the highest stat that would result in a Pokémon recieving this characteristic when divided by 5 | list integer                       |
| descriptions    | The descriptions of this characteristic listed in different languages                                                  | list [Description](#description)   |

## Egg Groups
Egg Groups are categories which determine which Pokémon are able to interbreed. Pokémon may belong to either one or two Egg Groups. Check out [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Egg_Group) for greater detail.

### GET api/v2/egg-group/{id or name}

###### Example response

```json
{
	"id": 1,
	"name": "monster",
	"names": [{
		"name": "ã‹ã„ã˜ã‚…ã†",
		"language": {
			"name": "ja",
			"url": "http://pokeapi.co/api/v2/language/1/"
		}
	}],
	"pokemon_species": [{
		"name": "bulbasaur",
		"url": "http://pokeapi.co/api/v2/pokemon-species/1/"
	}]
}

```

###### Response models

#### EggGroup

| Name            | Description                                                      | Data Type                                                                       |
|:----------------|:-----------------------------------------------------------------|:--------------------------------------------------------------------------------|
| id              | The identifier for this egg group resource                       | integer                                                                         |
| name            | The name for this egg group resource                             | string                                                                          |
| names           | The name of this egg group listed in different languages         | list [Name](#resourcename)                                                      |
| pokemon_species | A list of all Pokémon species that are members of this egg group | list [NamedAPIResource](#namedapiresource) ([PokemonSpecies](#pokemon-species)) |

## Genders
Genders were introduced in Generation II for the purposes of breeding Pokémon but can also result in visual differences or even different evolutionary lines. Check out [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Gender) for greater detail.

### GET api/v2/gender/{id or name}

###### Example response

```json
{
	"id": 1,
	"name": "female",
	"pokemon_species_details": [{
		"rate": 1,
		"pokemon_species": {
			"name": "bulbasaur",
			"url": "http://pokeapi.co/api/v2/pokemon-species/1/"
		}
	}],
	"required_for_evolution": [{
		"name": "wormadam",
		"url": "http://pokeapi.co/api/v2/pokemon-species/413/"
	}]
}

```

###### Response models

#### Gender

| Name                    | Description                                                                                    | Data Type                                                                       |
|:------------------------|:-----------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------|
| id                      | The identifier for this gender resource                                                        | integer                                                                         |
| name                    | The name for this gender resource                                                              | string                                                                          |
| pokemon_species_details | A list of Pokémon species that can be this gender and how likely it is that they will be       | list [PokemonSpeciesGender](#pokemonspeciesgender)                              |
| required_for_evolution  | A list of Pokémon species that required this gender in order for a Pokémon to evolve into them | list [NamedAPIResource](#namedapiresource) ([PokemonSpecies](#pokemon-species)) |

#### PokemonSpeciesGender

| Name            | Description                                                               | Data Type                                                                  |
|:----------------|:--------------------------------------------------------------------------|:---------------------------------------------------------------------------|
| rate            | The chance of this Pokémon being female, in eighths; or -1 for genderless | integer                                                                    |
| pokemon_species | A Pokémon species that can be the referenced gender                       | [NamedAPIResource](#namedapiresource) ([PokemonSpecies](#pokemon-species)) |

## Growth Rates
Growth rates are the speed with which Pokémon gain levels through experience. Check out [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Experience) for greater detail.

### GET api/v2/growth-rate/{id or name}

###### Example response

```json
{
	"id": 1,
	"name": "slow",
	"formula": "\\frac{5x^3}{4}",
	"descriptions": [{
		"description": "langsam",
		"language": {
			"name": "de",
			"url": "http://pokeapi.co/api/v2/language/6/"
		}
	}],
	"levels": [{
		"level": 100,
		"experience": 1250000
	}],
	"pokemon_species": [{
		"name": "growlithe",
		"url": "http://pokeapi.co/api/v2/pokemon-species/58/"
	}]
}
```

###### Response models

#### Growth Rate

| Name            | Description                                                                                   | Data Type                                                                       |
|:----------------|:----------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------|
| id              | The identifier for this gender resource                                                       | integer                                                                         |
| name            | The name for this gender resource                                                             | string                                                                          |
| formula         | The formula used to calculate the rate at which the Pokémon species gains level               | string                                                                          |
| descriptions    | The descriptions of this characteristic listed in different languages                         | list [Description](#description)                                                |
| levels          | A list of levels and the amount of experienced needed to atain them based on this growth rate | list [GrowthRateExperienceLevel](#growthrateexperiencelevel)                    |
| pokemon_species | A list of Pokémon species that gain levels at this growth rate                                | list [NamedAPIResource](#namedapiresource) ([PokemonSpecies](#pokemon-species)) |

#### GrowthRateExperienceLevel

| Name       | Description                                                     | Data Type |
|:-----------|:----------------------------------------------------------------|:----------|
| level      | The level gained                                                | integer   |
| experience | The amount of experience required to reach the referenced level | integer   |

## Natures
Natures influence how a Pokémon's stats grow. See [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Nature) for greater detail.

### GET api/v2/nature/{id or name}

###### Example response

```json
{
	"id": 2,
	"name": "bold",
	"decreased_stat": {
		"name": "attack",
		"url": "http://pokeapi.co/api/v2/stat/2/"
	},
	"increased_stat": {
		"name": "defense",
		"url": "http://pokeapi.co/api/v2/stat/3/"
	},
	"likes_flavor": {
		"name": "sour",
		"url": "http://pokeapi.co/api/v2/berry-flavor/5/"
	},
	"hates_flavor": {
		"name": "spicy",
		"url": "http://pokeapi.co/api/v2/berry-flavor/1/"
	},
	"pokeathlon_stat_changes": [{
		"max_change": -2,
		"pokeathlon_stat": {
			"name": "speed",
			"url": "http://pokeapi.co/api/v2/pokeathlon-stat/1/"
		}
	}],
	"move_battle_style_preferences": [{
		"low_hp_preference": 32,
		"high_hp_preference": 30,
		"move_battle_style": {
			"name": "attack",
			"url": "http://pokeapi.co/api/v2/move-battle-style/1/"
		}
	}],
	"names": [{
		"name": "ãšã¶ã¨ã„",
		"language": {
			"name": "ja",
			"url": "http://pokeapi.co/api/v2/language/1/"
		}
	}]
}
```

###### Response models

#### Nature

| Name                          | Description                                                                                                           | Data Type                                                             |
|:------------------------------|:----------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------|
| id                            | The identifier for this nature resource                                                                               | integer                                                               |
| name                          | The name for this nature resource                                                                                     | string                                                                |
| decreased_stat                | The stat decreased by 10% in Pokémon with this nature                                                                 | [NamedAPIResource](#namedapiresource) ([Stat](#stats))                |
| increased_stat                | The stat increased by 10% in Pokémon with this nature                                                                 | [NamedAPIResource](#namedapiresource) ([Stat](#stats))                |
| hates_flavor                  | The flavor hated by Pokémon with this nature                                                                          | [NamedAPIResource](#namedapiresource) ([BerryFlavor](#berry-flavors)) |
| likes_flavor                  | The flavor liked by Pokémon with this nature                                                                          | [NamedAPIResource](#namedapiresource) ([BerryFlavor](#berry-flavors)) |
| pokeathlon_stat_changes       | A list of Pokéathlon stats this nature effects and how much it effects them                                           | list [NatureStatChange](#naturestatchange)                            |
| move_battle_style_preferences | A list of battle styles and how likely a Pokémon with this nature is to use them in the Battle Palace or Battle Tent. | list [MoveBattleStylePreference](#movebattlestylepreference)          |
| names                         | The name of this nature listed in different languages                                                                 | list [Name](#resourcename)                                            |

#### NatureStatChange

| Name            | Description             | Data Type                                                                   |
|:----------------|:------------------------|:----------------------------------------------------------------------------|
| max_change      | The amount of change    | integer                                                                     |
| pokeathlon_stat | The stat being affected | [NamedAPIResource](#namedapiresource) ([PokeathlonStat](#pokeathlon-stats)) |

#### MoveBattleStylePreference

| Name               | Description                                                   | Data Type                                                                      |
|:-------------------|:--------------------------------------------------------------|:-------------------------------------------------------------------------------|
| low_hp_preference  | Chance of using the move, in percent, if HP is under one half | integer                                                                        |
| high_hp_preference | Chance of using the move, in percent, if HP is over one half  | integer                                                                        |
| move_battle_style  | The move battle style                                         | [NamedAPIResource](#namedapiresource) ([MoveBattleStyle](#move-battle-styles)) |

## Pokeathlon Stats
Pokeathlon Stats are different attributes of a Pokémon's performance in Pokéathlons. In Pokéathlons, competitions happen on different courses; one for each of the different Pokéathlon stats. See [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Pokéathlon) for greater detail.

### GET api/v2/pokeathlon-stat/{id or name}

###### Example response

```json
{
	"id": 1,
	"name": "speed",
	"affecting_natures": {
		"increase": [{
			"max_change": 2,
			"nature": {
				"name": "timid",
				"url": "http://pokeapi.co/api/v2/nature/5/"
			}
		}],
		"decrease": [{
			"max_change": -1,
			"nature": {
				"name": "hardy",
				"url": "http://pokeapi.co/api/v2/nature/1/"
			}
		}]
	},
	"names": [{
		"name": "Speed",
		"language": {
			"name": "en",
			"url": "http://pokeapi.co/api/v2/language/9/"
		}
	}]
}
```

###### Response models

#### PokeathlonStat

| Name              | Description                                                                    | Data Type                                                         |
|:------------------|:-------------------------------------------------------------------------------|:------------------------------------------------------------------|
| id                | The identifier for this Pokéathlon stat resource                               | integer                                                           |
| name              | The name for this Pokéathlon stat resource                                     | string                                                            |
| names             | The name of this Pokéathlon stat listed in different languages                 | list [Name](#resourcename)                                        |
| affecting_natures | A detail of natures which affect this Pokéathlon stat positively or negatively | [NaturePokeathlonStatAffectSets](#naturepokeathlonstataffectsets) |

#### NaturePokeathlonStatAffectSets

| Name     | Description                                                          | Data Type                                                      |
|:---------|:---------------------------------------------------------------------|:---------------------------------------------------------------|
| increase | A list of natures and how they change the referenced Pokéathlon stat | list [NaturePokeathlonStatAffect](#naturepokeathlonstataffect) |
| decrease | A list of natures and how they change the referenced Pokéathlon stat | list [NaturePokeathlonStatAffect](#naturepokeathlonstataffect) |

#### NaturePokeathlonStatAffect

| Name       | Description                                                    | Data Type                                                  |
|:-----------|:---------------------------------------------------------------|:-----------------------------------------------------------|
| max_change | The maximum amount of change to the referenced Pokéathlon stat | integer                                                    |
| nature     | The nature causing the change                                  | [NamedAPIResource](#namedapiresource) ([Nature](#natures)) |

## Pokemon
Pokémon are the creatures that inhabit the world of the Pokémon games. They can be caught using Pokéballs and trained by battling with other Pokémon. See [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Pokémon_(species)) for greater detail.

### GET api/v2/pokemon/{id or name}

###### Example response

```json
{
	"id": 12,
	"name": "butterfree",
	"base_experience": 178,
	"height": 11,
	"is_default": true,
	"order": 16,
	"weight": 320,
	"abilities": [{
		"is_hidden": true,
		"slot": 3,
		"ability": {
			"name": "tinted-lens",
			"url": "http://pokeapi.co/api/v2/ability/110/"
		}
	}],
	"forms": [{
		"name": "butterfree",
		"url": "http://pokeapi.co/api/v2/pokemon-form/12/"
	}],
	"game_indices": [{
		"game_index": 12,
		"version": {
			"name": "white-2",
			"url": "http://pokeapi.co/api/v2/version/22/"
		}
	}],
	"held_items": [{
		"item": {
			"name": "silver-powder",
			"url": "http://pokeapi.co/api/v2/item/199/"
		},
		"version_details": [{
			"rarity": 5,
			"version": {
				"name": "y",
				"url": "http://pokeapi.co/api/v2/version/24/"
			}
		}]
	}],
	"location_area_encounters": [{
		"location_area": {
			"name": "kanto-route-2-south-towards-viridian-city",
			"url": "http://pokeapi.co/api/v2/location-area/296/"
		},
		"version_details": [{
			"max_chance": 10,
			"encounter_details": [{
				"min_level": 7,
				"max_level": 7,
				"condition_values": [{
					"name": "time-morning",
					"url": "http://pokeapi.co/api/v2/encounter-condition-value/3/"
				}],
				"chance": 5,
				"method": {
					"name": "walk",
					"url": "http://pokeapi.co/api/v2/encounter-method/1/"
				}
			}],
			"version": {
				"name": "heartgold",
				"url": "http://pokeapi.co/api/v2/version/15/"
			}
		}]
	}],
	"moves": [{
		"move": {
			"name": "flash",
			"url": "http://pokeapi.co/api/v2/move/148/"
		},
		"version_group_details": [{
			"level_learned_at": 0,
			"version_group": {
				"name": "x-y",
				"url": "http://pokeapi.co/api/v2/version-group/15/"
			},
			"move_learn_method": {
				"name": "machine",
				"url": "http://pokeapi.co/api/v2/move-learn-method/4/"
			}
		}]
	}],
	"species": {
		"name": "butterfree",
		"url": "http://pokeapi.co/api/v2/pokemon-species/12/"
	},
	"sprites": {
		"back_female": "http://pokeapi.co/media/sprites/pokemon/back/female/12.png",
		"back_shiny_female": "http://pokeapi.co/media/sprites/pokemon/back/shiny/female/12.png",
		"back_default": "http://pokeapi.co/media/sprites/pokemon/back/12.png",
		"front_female": "http://pokeapi.co/media/sprites/pokemon/female/12.png",
		"front_shiny_female": "http://pokeapi.co/media/sprites/pokemon/shiny/female/12.png",
		"back_shiny": "http://pokeapi.co/media/sprites/pokemon/back/shiny/12.png",
		"front_default": "http://pokeapi.co/media/sprites/pokemon/12.png",
		"front_shiny": "http://pokeapi.co/media/sprites/pokemon/shiny/12.png"
	},
	"stats": [{
		"base_stat": 70,
		"effort": 0,
		"stat": {
			"name": "speed",
			"url": "http://pokeapi.co/api/v2/stat/6/"
		}
	}],
	"types": [{
		"slot": 2,
		"type": {
			"name": "flying",
			"url": "http://pokeapi.co/api/v2/type/3/"
		}
	}]
}
```

###### Response models

#### Pokemon

| Name                     | Description                                                                                      | Data Type                                                                  |
|:-------------------------|:-------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------|
| id                       | The identifier for this Pokémon resource                                                         | integer                                                                    |
| name                     | The name for this Pokémon resource                                                               | string                                                                     |
| base_experience          | The base experience gained for defeating this Pokémon                                            | integer                                                                    |
| height                   | The height of this Pokémon                                                                       | integer                                                                    |
| is_default               | Set for exactly one Pokémon used as the default for each species                                 | boolean                                                                    |
| order                    | Order for sorting. Almost national order, except families are grouped together.                  | integer                                                                    |
| weight                   | The weight of this Pokémon                                                                       | integer                                                                    |
| abilities                | A list of abilities this Pokémon could potentially have                                          | list [PokemonAbility](#pokemonability)                                     |
| forms                    | A list of forms this Pokémon can take on                                                         | list [NamedAPIResource](#namedapiresource) ([PokemonForm](#pokemon-forms)) |
| game_indices             | A list of game indices relevent to Pokémon item by generation                                    | list [VersionGameIndex](#versiongameindex)                                 |
| held_items               | A list of items this Pokémon may be holding when encountered                                     | list [PokemonHeldItem](#pokemonhelditem)                                   |
| location_area_encounters | A link to a list of location areas as well as encounter details pertaining to specific versions  | string (URL to list [LocationAreaEncounter](#locationareaencounter))       |
| moves                    | A list of moves along with learn methods and level details pertaining to specific version groups | list [PokemonMove](#pokemonmove)                                           |
| sprites                  | A set of sprites used to depict this Pokémon in the game                                         | [PokemonSprites](#pokemonsprites)                                          |
| species                  | The species this Pokémon belongs to                                                              | [NamedAPIResource](#namedapiresource) ([PokemonSpecies](#pokemon-species)) |
| stats                    | A list of base stat values for this Pokémon                                                      | list [PokemonStat](#pokemonstat)                                           |
| types                    | A list of details showing types this Pokémon has                                                 | list [PokemonType](#pokemontype)                                           |

#### PokemonAbility

| Name      | Description                                            | Data Type                                                     |
|:----------|:-------------------------------------------------------|:--------------------------------------------------------------|
| is_hidden | Whether or not this is a hidden ability                | boolean                                                       |
| slot      | The slot this ability occupies in this Pokémon species | integer                                                       |
| ability   | The ability the Pokémon may have                       | [NamedAPIResource](#namedapiresource) ([Ability](#abilities)) |

#### PokemonType

| Name | Description                                 | Data Type                                             |
|:-----|:--------------------------------------------|:------------------------------------------------------|
| slot | The order the Pokémon's types are listed in | integer                                               |
| type | The type the referenced Pokémon has         | [NamedAPIResource](#namedapiresource) ([Type](#type)) |

#### PokemonHeldItem

| Name            | Description                                                     | Data Type                                              |
|:----------------|:----------------------------------------------------------------|:-------------------------------------------------------|
| item            | The item the referenced Pokémon holds                           | [NamedAPIResource](#namedapiresource) ([Item](#item))  |
| version_details | The details of the different versions in which the item is held | list [PokemonHeldItemVersion](#pokemonhelditemversion) |

#### PokemonHeldItemVersion

| Name    | Description                           | Data Type                                                   |
|:--------|:--------------------------------------|:------------------------------------------------------------|
| version | The version in which the item is held | [NamedAPIResource](#namedapiresource) ([Version](#version)) |
| rarity  | How often the item is held            | integer                                                     |

#### PokemonMove

| Name                  | Description                                                        | Data Type                                             |
|:----------------------|:-------------------------------------------------------------------|:------------------------------------------------------|
| move                  | The move the Pokémon can learn                                     | [NamedAPIResource](#namedapiresource) ([Move](#move)) |
| version_group_details | The details of the version in which the Pokémon can learn the move | list [PokemonMoveVersion](#pokemonmoveversion)        |

#### PokemonMoveVersion

| Name              | Description                                    | Data Type                                                                     |
|:------------------|:-----------------------------------------------|:------------------------------------------------------------------------------|
| move_learn_method | The method by which the move is learned        | [NamedAPIResource](#namedapiresource) ([MoveLearnMethod](#move-learn-method)) |
| version_group     | The version group in which the move is learned | [NamedAPIResource](#namedapiresource) ([VersionGroup](#version-group))        |
| level_learned_at  | The minimum level to learn the move            | integer                                                                       |

#### PokemonStat

| Name      | Description                                        | Data Type                                             |
|:----------|:---------------------------------------------------|:------------------------------------------------------|
| stat      | The stat the Pokémon has                           | [NamedAPIResource](#namedapiresource) ([Stat](#stat)) |
| effort    | The effort points (EV) the Pokémon has in the stat | integer                                               |
| base_stat | The base value of the stst                         | integer                                               |

#### PokemonSprites

| Name               | Description                                                         | Data Type |
|:-------------------|:--------------------------------------------------------------------|:----------|
| front_default      | The default depiction of this Pokémon from the front in battle      | string    |
| front_shiny        | The shiny depiction of this Pokémon from the front in battle        | string    |
| front_female       | The female depiction of this Pokémon from the front in battle       | string    |
| front_shiny_female | The shiny female depiction of this Pokémon from the front in battle | string    |
| back_default       | The default depiction of this Pokémon from the back in battle       | string    |
| back_shiny         | The shiny depiction of this Pokémon from the back in battle         | string    |
| back_female        | The female depiction of this Pokémon from the back in battle        | string    |
| back_shiny_female  | The shiny female depiction of this Pokémon from the back in battle  | string    |

#### LocationAreaEncounter

| Name            | Description                                                                     | Data Type                                                          |
|:----------------|:--------------------------------------------------------------------------------|:-------------------------------------------------------------------|
| location_area   | The location area the referenced Pokémon can be encountered in                  | [NamedAPIResource](#apiresource) ([LocationArea](#location-areas)) |
| version_details | A list of versions and encounters with the referenced Pokémon that might happen | list [VersionEncounterDetail](#versionencounterdetail)             |

## Pokémon Colors
Colors used for sorting Pokémon in a Pokédex. The color listed in the Pokédex is usually the color most apparent or covering each Pokémon's body. No orange category exists; Pokémon that are primarily orange are listed as red or brown.

### GET api/v2/pokemon-color/{id or name}

###### Example response

```json
{
	"id": 1,
	"name": "black",
	"names": [{
		"name": "é»’ã„",
		"language": {
			"name": "ja",
			"url": "http://pokeapi.co/api/v2/language/1/"
		}
	}],
	"pokemon_species": [{
		"name": "snorlax",
		"url": "http://pokeapi.co/api/v2/pokemon-species/143/"
	}]
}
```

###### Response models

#### PokemonColor

| Name            | Description                                                  | Data Type                                                                       |
|:----------------|:-------------------------------------------------------------|:--------------------------------------------------------------------------------|
| id              | The identifier for this Pokémon color resource               | integer                                                                         |
| name            | The name for this Pokémon color resource                     | string                                                                          |
| names           | The name of this Pokémon color listed in different languages | list [Name](#resourcename)                                                      |
| pokemon_species | A list of the Pokémon species that have this color           | list [NamedAPIResource](#namedapiresource) ([PokemonSpecies](#pokemon-species)) |

## Pokémon Forms
Some Pokémon have the ability to take on different forms. At times, these differences are purely cosmetic and have no bearing on the difference in the Pokémon's stats from another; however, several Pokémon differ in stats (other than HP), type, and Ability depending on their form.

### GET api/v2/pokemon-form/{id or name}

###### example response

```json
{
	"id": 413,
	"name": "wormadam-plant",
	"order": 503,
	"form_order": 1,
	"is_default": true,
	"is_battle_only": false,
	"is_mega": false,
	"form_name": "plant",
	"pokemon": {
		"name": "wormadam-plant",
		"url": "http://pokeapi.co/api/v2/pokemon/413/"
	},
	"sprites": {
		"back_default": "http://pokeapi.co/media/sprites/pokemon/back/413.png",
		"back_shiny": "http://pokeapi.co/media/sprites/pokemon/back/shiny/413.png",
		"front_default": "http://pokeapi.co/media/sprites/pokemon/413.png",
		"front_shiny": "http://pokeapi.co/media/sprites/pokemon/shiny/413.png"
	},
	"version_group": {
		"name": "diamond-pearl",
		"url": "http://pokeapi.co/api/v2/version-group/8/"
	}
}
```

###### response models

#### PokemonForm

| Name           | Description                                                                                                                                              | Data Type                                                               |
|:---------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------|
| id             | The identifier for this Pokémon form resource                                                                                                            | integer                                                                 |
| name           | The name for this Pokémon form resource                                                                                                                  | string                                                                  |
| order          | The order in which forms should be sorted within all forms. Multiple forms may have equal order, in which case they should fall back on sorting by name. | integer                                                                 |
| form_order     | The order in which forms should be sorted within a species' forms                                                                                        | integer                                                                 |
| is_default     | True for exactly one form used as the default for each Pokémon                                                                                           | boolean                                                                 |
| is_battle_only | Whether or not this form can only happen during battle                                                                                                   | boolean                                                                 |
| is_mega        | Whether or not this form requires mega evolution                                                                                                         | boolean                                                                 |
| form_name      | The name of this form                                                                                                                                    | string                                                                  |
| pokemon        | The Pokémon that can take on this form                                                                                                                   | [NamedAPIResource](#namedapiresource) ([Pokemon](#pokemon))             |
| sprites        | A set of sprites used to depict this Pokémon form in the game                                                                                            | [PokemonFormSprites](#pokemonformsprites)                               |
| version_group  | The version group this Pokémon form was introduced in                                                                                                    | [NamedAPIResource](#namedapiresource) ([VersionGroup](#version-groups)) |
| names          | The form specific full name of this Pokémon form, or empty if the form does not have a specific name                                                     | list [Name](#name)                                                      |
| form_names     | The form specific form name of this Pokémon form, or empty if the form does not have a specific name                                                     | list [Name](#name)                                                      |

#### PokemonFormSprites

| Name          | Description                                                         | Data Type |
|:--------------|:--------------------------------------------------------------------|:----------|
| front_default | The default depiction of this Pokémon form from the front in battle | string    |
| front_shiny   | The shiny depiction of this Pokémon form from the front in battle   | string    |
| back_default  | The default depiction of this Pokémon form from the back in battle  | string    |
| back_shiny    | The shiny depiction of this Pokémon form from the back in battle    | string    |

## Pokémon Habitats
Habitats are generally different terrain Pokémon can be found in but can also be areas designated for rare or legendary Pokémon.

### GET api/v2/pokemon-habitat/{id or name}

###### Example response

```json
{
    "id": 1,
    "name": "cave",
    "names": [
        {
            "name": "grottes",
            "language": {
                "name": "fr",
                "url": "http://pokeapi.co/api/v2/language/5/"
            }
        }
    ],
    "pokemon_species": [
        {
            "name": "zubat",
            "url": "http://pokeapi.co/api/v2/pokemon-species/41/"
        }
    ]
}
```

###### Response models

#### PokemonHabitat

| Name            | Description                                                     | Data Type                                                                       |
|:----------------|:----------------------------------------------------------------|:--------------------------------------------------------------------------------|
| id              | The identifier for this Pokémon habitat resource                | integer                                                                         |
| name            | The name for this Pokémon habitat resource                      | string                                                                          |
| names           | The name of this Pokémon habitat listed in different languages  | list [Name](#resourcename)                                                      |
| pokemon_species | A list of the Pokémon species that can be found in this habitat | list [NamedAPIResource](#namedapiresource) ([PokemonSpecies](#pokemon-species)) |

## Pokémon Shapes
Shapes used for sorting Pokémon in a Pokédex.

### GET api/v2/pokemon-shape/{id or name}

###### Example response

```json
{
    "id": 1,
    "name": "ball",
    "awesome_names": [
        {
            "awesome_name": "Pomaceous",
            "language": {
                "name": "en",
                "url": "http://pokeapi.co/api/v2/language/9/"
            }
        }
    ],
    "names": [
        {
            "name": "Ball",
            "language": {
                "name": "en",
                "url": "http://pokeapi.co/api/v2/language/9/"
            }
        }
    ],
    "pokemon_species": [
        {
            "name": "shellder",
            "url": "http://pokeapi.co/api/v2/pokemon-species/90/"
        }
    ]
}
```

###### Response models

#### PokemonShape

| Name            | Description                                                               | Data Type                                                                       |
|:----------------|:--------------------------------------------------------------------------|:--------------------------------------------------------------------------------|
| id              | The identifier for this Pokémon shape resource                            | integer                                                                         |
| name            | The name for this Pokémon shape resource                                  | string                                                                          |
| awesome_names   | The "scientific" name of this Pokémon shape listed in different languages | list [AwesomeName](#awesomename)                                                |
| names           | The name of this Pokémon shape listed in different languages              | list [Name](#resourcename)                                                      |
| pokemon_species | A list of the Pokémon species that have this shape                        | list [NamedAPIResource](#namedapiresource) ([PokemonSpecies](#pokemon-species)) |

#### AwesomeName

| Name         | Description                                                                | Data Type                                                      |
|:-------------|:---------------------------------------------------------------------------|:---------------------------------------------------------------|
| awesome_name | The localized "scientific" name for an API resource in a specific language | string                                                         |
| language     | The language this "scientific" name is in                                  | [NamedAPIResource](#namedapiresource) ([Language](#languages)) |

## Pokémon Species
A Pokémon Species forms the basis for at least one Pokémon. Attributes of a Pokémon species are shared across all varieties of Pokémon within the species. A good example is Wormadam; Wormadam is the species which can be found in three different varieties, Wormadam-Trash, Wormadam-Sandy and Wormadam-Plant.

### GET api/v2/pokemon-species/{id or name}

###### Example response

```json
{
	"id": 413,
	"name": "wormadam",
	"order": 441,
	"gender_rate": 8,
	"capture_rate": 45,
	"base_happiness": 70,
	"is_baby": false,
	"hatch_counter": 15,
	"has_gender_differences": false,
	"forms_switchable": false,
	"growth_rate": {
		"name": "medium",
		"url": "http://pokeapi.co/api/v2/growth-rate/2/"
	},
	"pokedex_numbers": [{
		"entry_number": 45,
		"pokedex": {
			"name": "kalos-central",
			"url": "http://pokeapi.co/api/v2/pokedex/12/"
		}
	}],
	"egg_groups": [{
		"name": "bug",
		"url": "http://pokeapi.co/api/v2/egg-group/3/"
	}],
	"color": {
		"name": "gray",
		"url": "http://pokeapi.co/api/v2/pokemon-color/4/"
	},
	"shape": {
		"name": "squiggle",
		"url": "http://pokeapi.co/api/v2/pokemon-shape/2/"
	},
	"evolves_from_species": {
		"name": "burmy",
		"url": "http://pokeapi.co/api/v2/pokemon-species/412/"
	},
	"evolution_chain": {
		"url": "http://pokeapi.co/api/v2/evolution-chain/213/"
	},
	"habitat": null,
	"generation": {
		"name": "generation-iv",
		"url": "http://pokeapi.co/api/v2/generation/4/"
	},
	"names": [{
		"name": "Wormadam",
		"language": {
			"name": "en",
			"url": "http://pokeapi.co/api/v2/language/9/"
		}
	}],
	"flavor_text_entries": [
    {
        "flavor_text": "When the bulb on\nits back grows\nlarge, it appears\fto lose the\nability to stand\non its hind legs.",
        "language": {
            "name": "en",
            "url": "http://pokeapi.co/api/v2/language/9/"
        },
        "version": {
            "name": "red",
            "url": "http://pokeapi.co/api/v2/version/1/"
        }
    }],
	"form_descriptions": [{
		"description": "Forms have different stats and movepools.  During evolution, Burmy's current cloak becomes Wormadam's form, and can no longer be changed.",
		"language": {
			"name": "en",
			"url": "http://pokeapi.co/api/v2/language/9/"
		}
	}],
	"genera": [{
		"genus": "Bagworm",
		"language": {
			"name": "en",
			"url": "http://pokeapi.co/api/v2/language/9/"
		}
	}],
	"varieties": [{
		"is_default": true,
		"pokemon": {
			"name": "wormadam-plant",
			"url": "http://pokeapi.co/api/v2/pokemon/413/"
		}
	}]
}
```

###### Response models

#### PokemonSpecies

| Name                   | Description                                                                                                                                        | Data Type                                                                   |
|:-----------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------|
| id                     | The identifier for this Pokémon species resource                                                                                                   | integer                                                                     |
| name                   | The name for this Pokémon species resource                                                                                                         | string                                                                      |
| order                  | The order in which species should be sorted.  Based on National Dex order, except families are grouped together and sorted by stage.               | integer                                                                     |
| gender_rate            | The chance of this Pokémon being female, in eighths; or -1 for genderless                                                                          | integer                                                                     |
| capture_rate           | The base capture rate; up to 255. The higher the number, the easier the catch.                                                                     | integer                                                                     |
| base_happiness         | The happiness when caught by a normal Pokéball; up to 255. The higher the number, the happier the Pokémon.                                         | integer                                                                     |
| is_baby                | Whether or not this is a baby Pokémon                                                                                                              | boolean                                                                     |
| hatch_counter          | Initial hatch counter: one must walk 255 × (hatch_counter + 1) steps before this Pokémon's egg hatches, unless utilizing bonuses like Flame Body's | integer                                                                     |
| has_gender_differences | Whether or not this Pokémon has visual gender differences                                                                                     | boolean                                                                     |
| forms_switchable       | Whether or not this Pokémon has multiple forms and can switch between them                                                                         | boolean                                                                     |
| growth_rate            | The rate at which this Pokémon species gains levels                                                                                                | [NamedAPIResource](#namedapiresource) ([GrowthRate](#growth-rates))         |
| pokedex_numbers        | A list of Pokedexes and the indexes reserved within them for this Pokémon species                                                                  | list [PokemonSpeciesDexEntry](#pokemonspeciesdexentry)                      |
| egg_groups             | A list of egg groups this Pokémon species is a member of                                                                                           | list [NamedAPIResource](#namedapiresource) ([EggGroup](#egg-groups))        |
| color                  | The color of this Pokémon for gimmicky Pokédex search                                                                                              | [NamedAPIResource](#namedapiresource) ([PokemonColor](#pokemon-colors))     |
| shape                  | The shape of this Pokémon for gimmicky Pokédex search                                                                                              | [NamedAPIResource](#namedapiresource) ([PokemonShape](#pokemon-shapes))     |
| evolves_from_species   | The Pokémon species that evolves into this Pokemon_species                                                                                         | [NamedAPIResource](#namedapiresource) ([PokemonSpecies](#pokemon-species))  |
| evolution_chain        | The evolution chain this Pokémon species is a member of                                                                                            | [APIResource](#apiresource) ([EvolutionChain](#evolution-chains))           |
| habitat                | The habitat this Pokémon species can be encountered in                                                                                             | [NamedAPIResource](#namedapiresource) ([PokemonHabitat](#pokemon-habitats)) |
| generation             | The generation this Pokémon species was introduced in                                                                                              | [NamedAPIResource](#namedapiresource) ([Generation](#generations))          |
| names                  | The name of this Pokémon species listed in different languages                                                                                     | list [Name](#resourcename)                                                  |
| pal_park_encounters    | A list of encounters that can be had with this Pokémon species in pal park                                                                         | list [PalParkEncounterArea](#palparkencounterarea)                          |
| flavor_text_entries    | A list of flavor text entries for this Pokémon species                                                                                             | list [FlavorText](#flavortext)                                              |
| form_descriptions      | Descriptions of different forms Pokémon take on within the Pokémon species                                                                         | list [Description](#description)                                            |
| genera                 | The genus of this Pokémon species listed in multiple languages                                                                                     | list [Genus](#genus)                                                        |
| varieties              | A list of the Pokémon that exist within this Pokémon species                                                                                       | list [PokemonSpeciesVariety](#pokemonspeciesvariety)                        |

#### Genus

| Name     | Description                                            | Data Type                                                      |
|:---------|:-------------------------------------------------------|:---------------------------------------------------------------|
| genus    | The localized genus for the referenced Pokémon species | string                                                         |
| language | The language this genus is in                          | [NamedAPIResource](#namedapiresource) ([Language](#languages)) |

#### PokemonSpeciesDexEntry

| Name         | Description                                                | Data Type                                                     |
|:-------------|:-----------------------------------------------------------|:--------------------------------------------------------------|
| entry_number | The index number within the Pokédex                        | integer                                                       |
| pokedex      | The Pokédex the referenced Pokémon species can be found in | [NamedAPIResource](#namedapiresource) ([Pokedex](#pokedexes)) |

#### PalParkEncounterArea

| Name       | Description                                                                                    | Data Type                                                              |
|:-----------|:-----------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------|
| base_score | The base score given to the player when the referenced Pokémon is caught during a pal park run | integer                                                                |
| rate       | The base rate for encountering the referenced Pokémon in this pal park area                    | integer                                                                |
| area       | The pal park area where this encounter happens                                                 | [NamedAPIResource](#namedapiresource) ([PalParkArea](#pal-park-areas)) |

#### PokemonSpeciesVariety

| Name       | Description                                 | Data Type                                                   |
|:-----------|:--------------------------------------------|:------------------------------------------------------------|
| is_default | Whether this variety is the default variety | boolean                                                     |
| pokemon    | The Pokémon variety                         | [NamedAPIResource](#namedapiresource) ([Pokemon](#pokemon)) |

## Stats
Stats determine certain aspects of battles. Each Pokémon has a value for each stat which grows as they gain levels and can be altered momentarily by effects in battles.

### GET api/v2/stat/{id or name}

###### Example response

```json
{
	"id": 2,
	"name": "attack",
	"game_index": 2,
	"is_battle_only": false,
	"affecting_moves": {
		"increase": [{
			"change": 2,
			"move": {
				"name": "swords-dance",
				"url": "http://pokeapi.co/api/v2/move/14/"
			}
		}],
		"decrease": [{
			"change": -1,
			"move": {
				"name": "growl",
				"url": "http://pokeapi.co/api/v2/move/45/"
			}
		}]
	},
	"affecting_natures": {
		"increase": [{
			"name": "lonely",
			"url": "http://pokeapi.co/api/v2/nature/6/"
		}],
		"decrease": [{
			"name": "bold",
			"url": "http://pokeapi.co/api/v2/nature/2/"
		}]
	},
	"characteristics": [{
		"url": "http://pokeapi.co/api/v2/characteristic/2/"
	}],
	"move_damage_class": {
		"name": "physical",
		"url": "http://pokeapi.co/api/v2/move-damage-class/2/"
	},
	"names": [{
		"name": "ã“ã†ã’ã",
		"language": {
			"name": "ja",
			"url": "http://pokeapi.co/api/v2/language/1/"
		}
	}]
}
```

###### Response models

#### Stat

| Name              | Description                                                                                 | Data Type                                                                       |
|:------------------|:--------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------|
| id                | The identifier for this stat resource                                                       | integer                                                                         |
| name              | The name for this stat resource                                                             | string                                                                          |
| game_index        | ID the games use for this stat                                                              | integer                                                                         |
| is_battle_only    | Whether this stat only exists within a battle                                               | boolean                                                                         |
| affecting_moves   | A detail of moves which affect this stat positively or negatively                           | [MoveStatAffectSets](#movestataffectsets)                                       |
| affecting_natures | A detail of natures which affect this stat positively or negatively                         | [NatureStatAffectSets](#naturestataffectsets)                                   |
| characteristics   | A list of characteristics that are set on a Pokémon when its highest base stat is this stat | list [APIResource](#apiresource) ([Characteristic](#characteristics))           |
| move_damage_class | The class of damage this stat is directly related to                                        | [NamedAPIResource](#namedapiresource) ([MoveDamageClass](#move-damage-classes)) |
| names             | The name of this region listed in different languages                                       | list [Name](#resourcename)                                                      |

#### MoveStatAffectSets

| Name     | Description                                             | Data Type                              |
|:---------|:--------------------------------------------------------|:---------------------------------------|
| increase | A list of moves and how they change the referenced stat | list [MoveStatAffect](#movestataffect) |
| decrease | A list of moves and how they change the referenced stat | list [MoveStatAffect](#movestataffect) |

#### MoveStatAffect

| Name   | Description                                         | Data Type                                              |
|:-------|:----------------------------------------------------|:-------------------------------------------------------|
| change | The maximum amount of change to the referenced stat | integer                                                |
| move   | The move causing the change                         | [NamedAPIResource](#namedapiresource) ([Move](#moves)) |

#### NatureStatAffectSets

| Name     | Description                                               | Data Type                                                       |
|:---------|:----------------------------------------------------------|:----------------------------------------------------------------|
| increase | A list of natures and how they change the referenced stat | list [NamedAPIResource](#namedapiresource) ([Nature](#natures)) |
| decrease | A list of nature sand how they change the referenced stat | list [NamedAPIResource](#namedapiresource) ([Nature](#natures)) |

## Types
Types are properties for Pokémon and their moves. Each type has three properties: which types of Pokémon it is super effective against, which types of Pokémon it is not very effective against, and which types of Pokémon it is completely ineffective against.

### GET api/v2/type/{id or name}

###### Example response

```json
{
	"id": 5,
	"name": "ground",
	"damage_relations": {
		"no_damage_to": [{
			"name": "flying",
			"url": "http://pokeapi.co/api/v2/type/3/"
		}],
		"half_damage_to": [{
			"name": "bug",
			"url": "http://pokeapi.co/api/v2/type/7/"
		}],
		"double_damage_to": [{
			"name": "poison",
			"url": "http://pokeapi.co/api/v2/type/4/"
		}],
		"no_damage_from": [{
			"name": "electric",
			"url": "http://pokeapi.co/api/v2/type/13/"
		}],
		"half_damage_from": [{
			"name": "poison",
			"url": "http://pokeapi.co/api/v2/type/4/"
		}],
		"double_damage_from": [{
			"name": "water",
			"url": "http://pokeapi.co/api/v2/type/11/"
		}]
	},
	"game_indices": [{
		"game_index": 4,
		"generation": {
			"name": "generation-i",
			"url": "http://pokeapi.co/api/v2/generation/1/"
		}
	}],
	"generation": {
		"name": "generation-i",
		"url": "http://pokeapi.co/api/v2/generation/1/"
	},
	"move_damage_class": {
		"name": "physical",
		"url": "http://pokeapi.co/api/v2/move-damage-class/2/"
	},
	"names": [{
		"name": "ã˜ã‚ã‚“",
		"language": {
			"name": "ja",
			"url": "http://pokeapi.co/api/v2/language/1/"
		}
	}],
	"pokemon": [{
		"slot": 1,
		"pokemon": {
			"name": "sandshrew",
			"url": "http://pokeapi.co/api/v2/pokemon/27/"
		}
	}],
	"moves": [{
		"name": "sand-attack",
		"url": "http://pokeapi.co/api/v2/move/28/"
	}]
}
```

###### Response models

#### Type

| Name              | Description                                                         | Data Type                                                                       |
|:------------------|:--------------------------------------------------------------------|:--------------------------------------------------------------------------------|
| id                | The identifier for this type resource                               | integer                                                                         |
| name              | The name for this type resource                                     | string                                                                          |
| damage_relations  | A detail of how effective this type is toward others and vice versa | [TypeRelations](#typerelations)                                                 |
| game_indices      | A list of game indices relevent to this item by generation          | list [GenerationGameIndex](#generationgameindex)                                |
| generation        | The generation this type was introduced in                          | [NamedAPIResource](#namedapiresource) ([Generation](#generations))              |
| move_damage_class | The class of damage inflicted by this type                          | [NamedAPIResource](#namedapiresource) ([MoveDamageClass](#move-damage-classes)) |
| names             | The name of this type listed in different languages                 | list [Name](#resourcename)                                                      |
| pokemon           | A list of details of Pokémon that have this type                    | list [TypePokemon](#typepokemon)                                                |
| moves             | A list of moves that have this type                                 | list [NamedAPIResource](#namedapiresource) ([Move](#moves))                     |

#### TypePokemon

| Name    | Description                                 | Data Type                                                   |
|:--------|:--------------------------------------------|:------------------------------------------------------------|
| slot    | The order the Pokémon's types are listed in | integer                                                     |
| pokemon | The Pokémon that has the referenced type    | [NamedAPIResource](#namedapiresource) ([Pokemon](#pokemon)) |

#### TypeRelations

| Name               | Description                                                   | Data Type                                                   |
|:-------------------|:--------------------------------------------------------------|:------------------------------------------------------------|
| no_damage_to       | A list of types this type has no effect on                    | list [NamedAPIResource](#namedapiresource) ([Type](#types)) |
| half_damage_to     | A list of types this type is not very effect against          | list [NamedAPIResource](#namedapiresource) ([Type](#types)) |
| double_damage_to   | A list of types this type is very effect against              | list [NamedAPIResource](#namedapiresource) ([Type](#types)) |
| no_damage_from     | A list of types that have no effect on this type              | list [NamedAPIResource](#namedapiresource) ([Type](#types)) |
| half_damage_from   | A list of types that are not very effective against this type | list [NamedAPIResource](#namedapiresource) ([Type](#types)) |
| double_damage_from | A list of types that are very effective against this type     | list [NamedAPIResource](#namedapiresource) ([Type](#types)) |

<h1 id="utility-section">Utility</h1>

## Languages
Languages for translations of API resource information.

### GET api/v2/language/{id or name}

###### example response

```json
{
	"id": 1,
	"name": "ja",
	"official": true,
	"iso639": "ja",
	"iso3166": "jp",
	"names": [{
		"name": "Japanese",
		"language": {
			"name": "en",
			"url": "http://pokeapi.co/api/v2/language/9/"
		}
	}]
}
```

###### response models

#### Language

| Name     | Description                                                                                   | Data Type                  |
|:---------|:----------------------------------------------------------------------------------------------|:---------------------------|
| id       | The identifier for this language resource                                                     | integer                    |
| name     | The name for this language resource                                                           | string                     |
| official | Whether or not the games are published in this language                                       | boolean                    |
| iso639   | The two-letter code of the country where this language is spoken. Note that it is not unique. | string                     |
| iso3166  | The two-letter code of the language. Note that it is not unique.                              | string                     |
| names    | The name of this language listed in different languages                                       | list [Name](#resourcename) |

## Common Models

#### APIResource

| Name | Description                        | Data Type |
|:-----|:-----------------------------------|:----------|
| url  | The URL of the referenced resource | string    |

#### Description

| Name        | Description                                                          | Data Type                                                      |
|:------------|:---------------------------------------------------------------------|:---------------------------------------------------------------|
| description | The localized description for an API resource in a specific language | string                                                         |
| language    | The language this name is in                                         | [NamedAPIResource](#namedapiresource) ([Language](#languages)) |

#### Effect

| Name     | Description                                                          | Data Type                                                     |
|:---------|:---------------------------------------------------------------------|:--------------------------------------------------------------|
| effect   | The localized effect text for an API resource in a specific language | string                                                        |
| language | The language this effect is in                                       | [NamedAPIResource](#namedapiresource) ([Language](#language)) |

#### Encounter

| Name             | Description                                                                   | Data Type                                                                                           |
|:-----------------|:------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------|
| min_level        | The lowest level the Pokémon could be encountered at                          | integer                                                                                             |
| max_level        | The highest level the Pokémon could be encountered at                         | integer                                                                                             |
| condition_values | A list of condition values that must be in effect for this encounter to occur | list [NamedAPIResource](#namedapiresource) ([EncounterConditionValue](#encounter-condition-values)) |
| chance           | percent chance that this encounter will occur                                 | integer                                                                                             |
| method           | The method by which this encounter happens                                    | [NamedAPIResource](#namedapiresource) ([EncounterMethod](#encounter-methods))                       |

#### FlavorText

| Name        | Description                                                          | Data Type                                                      |
|:------------|:---------------------------------------------------------------------|:---------------------------------------------------------------|
| flavor_text | The localized flavor text for an API resource in a specific language | string                                                         |
| language    | The language this name is in                                         | [NamedAPIResource](#namedapiresource) ([Language](#languages)) |

#### GenerationGameIndex

| Name       | Description                                         | Data Type                                                          |
|:-----------|:----------------------------------------------------|:-------------------------------------------------------------------|
| game_index | The internal id of an API resource within game data | integer                                                            |
| generation | The generation relevent to this game index          | [NamedAPIResource](#namedapiresource) ([Generation](#generations)) |

#### MachineVersionDetail

| Name          | Description                                    | Data Type                                                   |
|:--------------|:-----------------------------------------------|:------------------------------------------------------------|
| machine       | The machine that teaches a move from an item   | [APIResource](#apiresource) ([Machine](#machines))           |
| version_group | The version group of this specific machine     | [NamedAPIResource](#namedapiresource) ([VersionGroup](#version-groups)) |

#### <a id="resourcename"></a>Name

| Name     | Description                                                   | Data Type                                                      |
|:---------|:--------------------------------------------------------------|:---------------------------------------------------------------|
| name     | The localized name for an API resource in a specific language | string                                                         |
| language | The language this name is in                                  | [NamedAPIResource](#namedapiresource) ([Language](#languages)) |

#### NamedAPIResource

| Name | Description                         | Data Type |
|:-----|:------------------------------------|:----------|
| name | The name of the referenced resource | string    |
| url  | The URL of the referenced resource  | string    |

#### VerboseEffect

| Name         | Description                                                          | Data Type                                                      |
|:-------------|:---------------------------------------------------------------------|:---------------------------------------------------------------|
| effect       | The localized effect text for an API resource in a specific language | string                                                         |
| short_effect | The localized effect text in brief                                   | string                                                         |
| language     | The language this effect is in                                       | [NamedAPIResource](#namedapiresource) ([Language](#languages)) |

#### VersionEncounterDetail

| Name              | Description                                     | Data Type                                                    |
|:------------------|:------------------------------------------------|:-------------------------------------------------------------|
| version           | The game version this encounter happens in      | [NamedAPIResource](#namedapiresource) ([Version](#versions)) |
| max_chance        | The total percentage of all encounter potential | integer                                                      |
| encounter_details | A list of encounters and their specifics        | list [Encounter](#encounters)                                |

#### VersionGameIndex

| Name       | Description                                         | Data Type                                                    |
|:-----------|:----------------------------------------------------|:-------------------------------------------------------------|
| game_index | The internal id of an API resource within game data | integer                                                      |
| version    | The version relevent to this game index             | [NamedAPIResource](#namedapiresource) ([Version](#versions)) |

#### VersionGroupFlavorText

| Name          | Description                                                   | Data Type                                                               |
|:--------------|:--------------------------------------------------------------|:------------------------------------------------------------------------|
| text          | The localized name for an API resource in a specific language | string                                                                  |
| language      | The language this name is in                                  | [NamedAPIResource](#namedapiresource) ([Language](#languages))          |
| version_group | The version group which uses this flavor text                 | [NamedAPIResource](#namedapiresource) ([VersionGroup](#version-groups)) |
