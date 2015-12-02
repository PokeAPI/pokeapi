# Pokeapi V2 API Reference

#### API Endpoints
[Abilities](#abilities)
[Berries](#berries)
[Berry Firmnesses](#berryfirmnesses)
[Berry Flavors](#berryflavors)
[Characteristics](#characteristics)
[Contest Types](#contesttypes)
[Contest Effects](#contesteffects)
[Egg Groups](#egggroups)
[Encounter Methods](#encountermethods)
[Encounter Conditions](#encounterconditions)
[Encounter Condition Values](#encounterconditionvalues)
[Evolution Chains](#evolutionchains)
[Evolution Triggers](#evolutiontriggers)
[Generation](#generations)
[Genders](#genders)
[Growth Rates](#abilities)
[Items](#items)
[Item Categories](#itemcategories)
[Item Attributes](#itemattributes)
[Item Fling Effects](#itemflingeffects)
[Item Pockets](#itempockets)
[Languages](#languages)
[Locations](#locations)
[Location Areas](#location areas)
[Moves](#moves)
[Move Ailments](#moveailments)
[Move Battle Styles](#movebattlestyles)
[Move Categories](#movecategories)
[Move Damage Classes](#movedamageclasses)
[Move Learn Methods](#movelearnmethods)
[Move Targets](#movetargets)
[Natures](#natures)
[Pal Park Areas](#palparkareas)
[Pokedexes](#pokedexes)
[Pokemon](#pokemon)
[Pokemon Colors](#pokemoncolors)
[Pokemon Forms](#pokemonforms)
[Pokemon Habitats](#pokemonhabitats)
[Pokemon Shapes](#pokemonshapes)
[Pokemon Species](#pokemonspecies)
[Pokeathlon Stats](#pokeathlonstats)
[Regions](#region)
[Stats](#stats)
[Super Contest Effects](#supercontesteffects)
[Types](#types)
[Versions](#versions)
[VersionGroups](#versiongroups)

## Abilities
```
api/v2/ability/{id or name}
```
Abilities provide passive effects for pokemon in battle or overworld. Pokemon can have only one ability at a time. Check out [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Ability) for greater detail.

###### example response
```json
{
	"id": 1,
	"name": "stench",
	"is_main_series": true,
	"generation": {
		"name": "generation-iii",
		"url": "http://localhost:8000/api/v2/generation/3/"
	},
	"names": [{
		"name": "Stench",
		"language": {
			"name": "en",
			"url": "http://localhost:8000/api/v2/language/9/"
		}
	}],
	"effect_entries": [{
		"effect": "This PokÃ©mon's damaging moves have a 10% chance to make the target [flinch]{mechanic:flinch} with each hit if they do not already cause flinching as a secondary effect.\n\nThis ability does not stack with a held item.\n\nOverworld: The wild encounter rate is halved while this PokÃ©mon is first in the party.",
		"short_effect": "Has a 10% chance of making target PokÃ©mon [flinch]{mechanic:flinch} with each hit.",
		"language": {
			"name": "en",
			"url": "http://localhost:8000/api/v2/language/9/"
		}
	}],
	"effect_changes": [{
		"version_group": {
			"name": "black-white",
			"url": "http://localhost:8000/api/v2/version-group/11/"
		},
		"effect_entries": [{
			"effect": "Has no effect in battle.",
			"language": {
				"name": "en",
				"url": "http://localhost:8000/api/v2/language/9/"
			}
		}]
	}],
	"flavor_text_entries": [{
		"flavor_text": "è‡­ãã¦ã€€ç›¸æ‰‹ãŒ\nã²ã‚‹ã‚€ã€€ã“ã¨ãŒã‚ã‚‹ã€‚",
		"language": {
			"name": "ja-kanji",
			"url": "http://localhost:8000/api/v2/language/11/"
		},
		"version_group": {
			"name": "x-y",
			"url": "http://localhost:8000/api/v2/version-group/15/"
		}
	}],
	"pokemon": [{
		"is_hidden": true,
		"slot": 3,
		"pokemon": {
			"name": "gloom",
			"url": "http://localhost:8000/api/v2/pokemon/44/"
		}
	}]
}
```

###### response models

#### Ability

Name | Description | Data Type
---- | ----------- | ---------
id                  | The identifier for this ability resource                                             | integer
name                | The name for this ability resource                                                   | string
is_main_series      | Whether or not this ability originated in the main series of the video games         | boolean
generation          | The generation this ability originated in                                            | [APIResource](#apiresource) ([Generation](#generations))
names               | The name of this ability listed in different languages                               | [[Name](#resourcename)]
effect_entries      | The effect of this ability listed in different languages                             | [[VerboseEffect](#verboseeffect)]
effect_changes      | The list of previous effects this ability has had across version groups of the games | [[AbilityEffectChange](#abilityeffectchange)]
flavor_text_entries | The flavor text of this ability listed in different languages                        | [VersionSpecificFlavorText] TODO
pokemon             | A list of pokemon that could potentially have this ability                           | [[AbilityPokemonMap](#abilitypokemonmap)]

#### AbilityEffectChange

Name | Description | Data Type
---- | ----------- | ---------
effect_entries | The previous effect of this ability listed in different languages         | [Effect]
version_group  | The version group in which the previous effect of this ability originated | [APIResource](#apiresource) ([VersionGroup](#versiongroups))

#### AbilityPokemonMap

Name | Description | Data Type
---- | ----------- | ---------
is_hidden | Whether or not this a hidden ability for the referenced pokemon                                                                                          | boolean
slot      | Pokemon have 3 ability 'slots' which hold references to possible abilities they could have. This is the slot of this ability for the referenced pokemon. | integer
pokemon   | The pokemon this ability could belong to                                                                                                                 | [APIResource](#apiresource) ([Pokemon](#pokemon))



## Berries
```
api/v2/berry/{id or name}
```
Berries are small fruits that can provide HP and status condition restoration, stat enhancement, and even damage negation when eaten by pokemon. Check out [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Berry) for greater detail.

Name | Description | Data Type
---- | ----------- | ---------
id                 | The identifier for this berry resource                                                                                | integer
name               | The name for this berry resource                                                                                      | string
growth_time        | TODO                                                                                                                  | integer
max_harvest        | TODO                                                                                                                  | integer
natural_gift_power | The strength of this powers natural gift                                                                              | integer
size               | The size of this berry                                                                                                | integer
smoothness         | The smoothness rating of this berry                                                                                   | integer
soil_dryness       | TODO                                                                                                                  | integer
firmness           | The firmness of this berry                                                                                            | [APIResource](#apiresource) ([BerryFirmness](#berryfirmnesses))
flavors            | A list of references to each flavor a berry can have and the potency of each of those flavors in regard to this berry | [[BerryFlavorMap](#berryflavormap)]
item               | Berries are actually items. This is a reference to the item specific data for this berry.                             | [APIResource](#apiresource) ([Item](#items))
natural_gift_type  | A reference to the elemental type of a this berry TODO                                                                | [APIResource](#apiresource) ([Type](#types))

#### BerryFlavorMap

Name | Description | Data Type
---- | ----------- | ---------
potency | How powerful the referenced flavor is for this berry | integer
flavor  | The referenced berry flavor                          | [APIResource](#apiresource) ([BerryFlavor](#berryflavors))



## Berry Firmnesses
```
api/v2/berry-firmness/{id or name}
```
TODO. Absolutely no idea what firmness does for a berry. Check out [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Berry) for greater detail.

Name | Description | Data Type
---- | ----------- | ---------
id      | The identifier for this berry firmness resource               | integer
name    | The name for this berry firmness resource                     | string
berries | A list of the berries with this firmness                      | [[APIResource](#apiresource) ([Berry](#berries))]
names   | The name of this berry firmness listed in different languages | [[Name](#resourcename)]



## Berry Flavors
```
api/v2/berry-flavor/{id or name}
```
Flavors determine whether a pokemon will benefit or suffer from eating a berry based on their [nature](#natures). Check out [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Flavor) for greater detail.

Name | Description | Data Type
---- | ----------- | ---------
id           | The identifier for this berry flavor resource               | integer
name         | The name for this berry flavor resource                     | string
berries      | A list of the berries with this flavor                      | [[APIResource](#apiresource) ([Berry](#berries))]
contest_type | TODO                                                        | [APIResource](#apiresource) ([ContestType](#contesttypes))
names        | The name of this berry flavor listed in different languages | [[Name](#resourcename)]
 


## Characteristics
```
api/v2/characteristic/{id}
```
Check out [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Characteristic) for greater detail.

Name | Description | Data Type
---- | ----------- | ---------
id              | The identifier for this characteristic resource                                                                                      | integer
gene_modulo     | The remainder of the highest stat divided by 5 TODO                                                                                  | integer
possible_values | The possible values of the highest stat that would result in a pokemon recieving this characteristic when divided by the gene modulo | [integer]
descriptions    | The descriptions of this characteristic listed in different languages                                                                | [[Description](#description)]



## Contest Types
```
api/v2/contest-type/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id           | The identifier for this contest type resource               | integer
name         | The name for this contest type resource                     | string
berry_flavor | TODO                                                        | [APIResource](#apiresource) ([BerryFlavor](#berryflavors))
names        | The name of this contest type listed in different languages | [[Name](#resourcename)]



## Contest Effects
```
api/v2/contest-effect/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id                  | The identifier for this contest type resource                        | integer
appeal              | The level of appeal this effect has TODO                             | string
jam                 | TODO                                                                 | integer
effect_entries      | The result of this contest effect listed in different languages      | [[Effect](#effect)]
flavor_text_entries | The flavor text of this contest effect listed in different languages | [[FlavorText](#flavortext)]



## Egg Groups
```
api/v2/egg-group/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id              | The identifier for this egg group resource                              | integer
name            | The name for this egg group resource                                    | string
names           | The name of this egg group listed in different languages                | [[Name](#resourcename)]
pokemon_species | A list of all pokemon species that are categorized under this egg group | [APIResource](#apiresource) ([PokemonSpecies](#pokemonspecies))



## Encounter Methods
```
api/v2/encounter-method/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id    | The identifier for this encounter method resource                         | integer
name  | The name for this encounter method resource                               | string
order | The order index of this encounter method within the main game series data | integer
names | The name of this encounter method listed in different languages           | [[Name](#resourcename)]



## Encounter Conditions
```
api/v2/encounter-condition/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id     | The identifier for this encounter condition resource            | integer
name   | The name for this encounter condition resource                  | string
names  | The name of this encounter method listed in different languages | [[Name](#resourcename)]
values | A list of possible values for this encounter condition          | [[APIReference](#apireference) ([EncounterConditionValue](#encounterconditionvalue))]



## Encounter Condition Values TODO
```
api/v2/encounter-condition-value/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id        | The identifier for this encounter condition value resource      | integer
name      | The name for this encounter condition value resource            | string
condition | The condition this encounter condition value pertains to        | [[APIReference](#apireference)]
names     | The name of this encounter method listed in different languages | [[Name](#resourcename)]



## Evolution Chains
```
api/v2/evolution-chain/{id}
```

Name | Description | Data Type
---- | ----------- | ---------
id                | The identifier for this evolution chain resource                                                                                                                   | integer
baby_trigger_item | The item that a pokemon would be holding when mating that would trigger the egg hatching a baby pokemon rather than a basic pokemon                                | [APIReference](#apireference) ([Item](#items))
chain             | The base chain link object. Each link contains evolution details for a pokemon in the chain. Each link references the next pokemon in the natural evolution order. | [ChainLink](#chainlink)

#### Chain Link

Name | Description | Data Type
---- | ----------- | ---------
is_baby           | Whether or not this link is for a baby pokemon. This would only ever be true on the base link. | boolean
species           | The pokemon species at this point in the evolution chain                                       | [APIReference](#apireference) ([PokemonSpecies](#pokemonspecies))
evolution_details | All details regarding the specific details of the referenced pokemon species evolution         | [EvolutionDetail](#evolutiondetail)
evolves_to        | A List of chain objects.                                                                       | [ChainLink](#chainlink)

#### Evolution Detail

Name | Description | Data Type
---- | ----------- | ---------
item                    | The item required to cause evolution this into pokemon species                                                                                                              | [APIReference](#apireference) ([Item](#items))
trigger                 | The type of event that triggers evolution into this pokemon species                                                                                                         | [APIReference](#apireference) ([EvolutionTrigger](#evolutiontriggers))
gender                  | The gender the evolving pokemon species must be in order to evolve into this pokemon species                                                                                | [APIReference](#apireference) ([Gender](#genders))
held_item               | The item the evolving pokemon species must be holding during the evolution trigger event to evolve into this pokemon species                                                | [APIReference](#apireference) ([Item](#items))
known_move              | The move that must be known by the evolving pokemon species during the evolution trigger event in order to evolve into this pokemon species                                 | [APIReference](#apireference) ([Move](#moves))
known_move_type         | The evolving pokemon species must know a move with this type during the evolution trigger event in order to evolve into this pokemon species                                | [APIReference](#apireference) ([Type](#types))
location                | The location the evolution must be triggered at.                                                                                                                            | [APIReference](#apireference) ([Location](#location))
min_level               | The minimum required level of the evolving pokemon species to evolve into this pokemon species                                                                              | integer
min_hapiness            | The minimum required level of happiness the evolving pokemon species to evolve into this pokemon species                                                                    | integer
min_beauty              | The minimum required level of beauty the evolving pokemon species to evolve into this pokemon species                                                                       | integer
min_affection           | The minimum required level of affection the evolving pokemon species to evolve into this pokemon species                                                                    | integer
needs_overworld_rain    | Whether or not it must be raining in the overworld to cause evolution this pokemon species                                                                                  | boolean
party_species           | The pokemon species that must be in the players party in order for the evolving pokemon species to evolve into this pokemon species                                         | [APIReference](#apireference) ([PokemonSpecies](#pokemonspecies))
party_type              | The player must have a pokemon of this type in their party during the evolution trigger event in order for the evolving pokemon species to evolve into this pokemon species | [APIReference](#apireference) ([Type](#types))
relative_physical_stats | The required relation between the Pokémon's Attack and Defense stats. 1 means Attack > Defense. 0 means Attack = Defense. -1 means Attack < Defense.                        | integer
time_of_day             | The required time of day. Day or night.                                                                                                                                     | string
trade_species           | Pokemon species for which this one must be traded.                                                                                                                          | [APIReference](#apireference) ([Pokemon Species](#pokemonspecies))
turn_upside_down        | Whether or not the 3DS needs to be turned upside-down as this Pokémon levels up.                                                                                            | boolean


## Encounter Triggers
```
api/v2/evolution-trigger/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id              | The identifier for this evolution trigger resource                | integer
name            | The name for this evolution trigger resource                      | string
names           | The name of this evolution trigger listed in different languages  | [[Name](#resourcename)]
pokemon_species | A list of pokemon species that result from this evolution trigger | [[APIReference](#apireference) ([PokemonSpecies](#pokemonspecies))]


## Generations
```
api/v2/generation/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id              | The identifier for this generation resource                       | integer
name            | The name for this generation resource                             | string
abilities       | A list of abilities that were introduced in this generation       | [[APIReference](#apireference) ([Ability](#abilities))]
names           | The name of this generation listed in different languages         | [[Name](#resourcename)]
main_region     | The main region travelled in this generation                      | [APIReference](#apireference) ([Region](#regions))
moves           | A list of moves that were introduced in this generation           | [[APIReference](#apireference) ([Move](#moves))]
pokemon_species | A list of pokemon species that were introduced in this generation | [[APIReference](#apireference) ([PokemonSpecies](#pokemonspecies))]
types           | A list of types that were introduced in this generation           | [[APIReference](#apireference) ([Type](#types))]
version_groups  | A list of version groups that were introduced in this generation  | [[APIReference](#apireference) ([VersionGroup](#versiongroups))]


## Gender
```
api/v2/gender/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id                      | The identifier for this gender resource                                                        | integer
name                    | The name for this gender resource                                                              | string
pokemon_species_details | A list of pokemon species that can be this gender and how likely it is that they will be       | [([PokemonSpeciesGenderChance](#pokemonspeciesgendermap)]
required_for_evolution  | A list of pokemon species that required this gender in order for a pokemon to evolve into them | [[APIReference](#apireference) ([PokemonSpecies](#pokemonspecies))]


#### PokemonSpeciesGenderChance

Name | Description | Data Type
---- | ----------- | ---------
rate            | The chance of this Pokémon being female, in eighths; or -1 for genderless | integer
pokemon_species | A pokemon species that can be the referenced gender                       | [APIReference](#apireference) ([PokemonSpecies](#pokemonspecies))


## Growth Rates
```
api/v2/growth-rate/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id              | The identifier for this gender resource                                                       | integer
name            | The name for this gender resource                                                             | string
formula         | The formula used to calculate the rate at which the pokemon species gains level               | string
descriptions    | The descriptions of this characteristic listed in different languages                         | [[Description](#description)]
levels          | A list of levels and the amount of experienced needed to atain them based on this growth rate | [[GrowthRateExperienceLevel](#growthrateexperiencelevel)]
pokemon_species | A list of pokemon species that gain levels at this growth rate                                | [[APIReference](#apireference) ([PokemonSpecies](#pokemonspecies))]

#### GrowthRateExperienceLevel

Name | Description | Data Type
---- | ----------- | ---------
level      | The level gained                                                | integer
experience | The amount of experience required to reach the referenced level | integer


## Items
```
api/v2/item/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id                  | The identifier for this item resource                                | integer
name                | The name for this item resource                                      | string
cost                | The price of this item in stores                                     | integer
fling_power         | The power of the move Fling when used with this item.                | integer
fling_effect        | The effect of the move Fling when used with this item                | [ItemFlingEffect](#itemflingeffect)
attributes          | A list of attributes this item has                                   | [[APIReference](#apireference) ([ItemAttribute](#itemattributes))]
category            | The category of items this item falls into                           | [ItemCategory](#itemcategory)
effect_entries      | The effect of this ability listed in different languages             | [[VerboseEffect](#verboseeffect)]
flavor_text_entries | The flavor text of this ability listed in different languages        | [VersionSpecificFlavorText] TODO
game_indices        | A list of game indices relevent to this item by generation           | [[GenerationGameIndex](#generationgameindex)]
names               | The name of this item listed in different languages                  | [[Name](#resourcename)]
held_by_pokemon     | A list of pokemon that might be found in the wild holding this item  | [[APIReference](#apireference) ([Pokemon](#pokemon))]
baby_trigger_for    | An evolution chain this item requires to produce a bay during mating | [[APIReference](#apireference) ([Evolution Chain](#evolutionchains))]


## Item Fling Effects
```
api/v2/item-fling-effect/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id             | The identifier for this fling effect resource                 | integer
name           | The name for this fling effect resource                       | string
effect_entries | The result of this fling effect listed in different languages | [[Effect](#effect)]
items          | A list of items that have this fling effect                   | [[Item](#item)]


## Item Categories
```
api/v2/item-category/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id     | The identifier for this item category resource               | integer
name   | The name for this item category resource                     | string
items  | A list of items that fall into this category                 | [[Item](#item)]
names  | The name of this item category listed in different languages | [[Name](#resourcename)]
pocket | The pocket items in this category would be put in            | [[APIReference](#apireference) ([ItemPocket](#itempockets))]


## Item Pockets
```
api/v2/item-pocket/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id         | The identifier for this item pocket resource                    | integer
name       | The name for this item pocket resource                          | string
categories | A list of item categories that are relevent to this item pocket | [[ItemCategory](#itemcategory)]
names      | The name of this item category listed in different languages    | [[Name](#resourcename)]


## Languages
```
api/v2/language/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id       | The identifier for this item pocket resource                                                  | integer
name     | The name for this item pocket resource                                                        | string
official | Whether or not the games are published in this language                                       | boolean
is639    | The two-letter code of the country where this language is spoken. Note that it is not unique. | string
iso3166  | The two-letter code of the language. Note that it is not unique.                              | string
names    | The name of this language listed in different languages                                       | [[Name](#resourcename)]


## Locations
```
api/v2/location/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id           | The identifier for this location resource                      | integer
name         | The name for this location resource                            | string
region       | The region this location can be found in                       | [APIReference](#apireference) ([Region](#regions))
names        | The name of this language listed in different languages        | [[Name](#resourcename)]
game_indices | A list of game indices relevent to this location by generation | [[GenerationGameIndex](#generationgameindex)]
areas        | Areas that can be found within this location                   | [APIReference](#apireference) ([LocationArea](#locationareas))


## Location Areas
```
api/v2/location-area/{id}
```

Name | Description | Data Type
---- | ----------- | ---------
id                     | The identifier for this location resource                                                                                                    | integer
name                   | The name for this location resource                                                                                                          | string
game_index             | The internal id of an api resource within game data                                                                                          | integer
encounter_method_rates | A list of methods in which pokemon may be encountered in this area and how likely the method will occur depending on the version of the game | [[EncounterMethodRate](#encountermethodrate)]
location               | The region this location can be found in                                                                                                     | [APIReference](#apireference) ([Region](#regions))
names                  | The name of this location area listed in different languages                                                                                 | [[Name](#resourcename)]
pokemon_encounters     | A list of pokemon that can be encountered in this area along with version specific details about the encounter                               | [PokemonEncounter](#pokemonencounter)

#### PokemonEncounter

Name | Description | Data Type
---- | ----------- | ---------
pokemon | The pokemon being encountered | [APIReference](#apireference) ([Pokemon](#pokemon))
version_group_details | A list of version groups and encounters with the referenced pokemon that might happen | [[VersionGroupEncounterDetail](#versiongroupencounterdetail)]

#### VersionGroupEncounterDetail

Name | Description | Data Type
---- | ----------- | ---------
version | The game version this encounter happens in | [APIReference](#apireference) ([Version](#versions))
max_chance | The total percentage of all encounter potential | integer
encounter_details | A list of encounters and their specifics | [[Encounter](#encounters)]


## Moves
```
api/v2/move/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id             | The identifier for this location resource                                                                                                                                 | integer
name           | The name for this location resource                                                                                                                                       | string
accuracy       | The percent value of how likely this move is to be successful                                                                                                             | integer
effect_chance  | The percent value of how likely it is this moves effect will take effect                                                                                                  | integer
pp             | Power points. The number of times this move can be used                                                                                                                   | integer
priority       | A value between -8 and 8. Sets the order in which moves are executed during battle. See [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Priority) for greater detail. | integer
power          | The base power of this move with a value of 0 if it does not have a base power                                                                                            | integer
contest_combos | A detail of normal and super contest combos that require this move                                                                                                        | [[ContestComboSets](#contestcombosets)]
contest_type   | The type of appeal this move gives a pokemon when used in a contest                                                                                                       | [APIReference](#apireference) ([ContestType](#contesttypes))
contest_effect | The effect the move has when used in a contest                                                                                                                            | [APIReference](#apireference) ([ContestEffect](#contesteffects))
damage_class   | The type of damage the move inflicts on the target, e.g. physical                                                                                                         | [APIReference](#apireference) ([MoveDamageClass](#movedamageclasses))
effect_entries | The effect of this move listed in different languages                                                                                                                     | [[VerboseEffect](#verboseeffect)]
effect_changes | The list of previous effects this move has had across version groups of the games                                                                                         | [[AbilityEffectChange](#abilityeffectchange)]
generation     | The generation in which this move was introduced                                                                                                                          | [APIReference](#apireference) ([Generation](#generations))
meta           | Meta data about this move                                                                                                                                                 | [MoveMetaData](#movemetadata)
names          | The name of this location area listed in different languages                                                                                                              | [[Name](#resourcename)]
past_values    | A list of move resource value changes across ersion groups of the game                                                                                                    | [PastMoveStatValues](#pastmovestatvalues)
stat_changes   | A list of stats this moves effects and how much it effects them                                                                                                           | [[MoveStatChange](#movestatchange)]
contest_effect | The effect the move has when used in a super contest                                                                                                                      | [APIReference](#apireference) ([ContestEffect](#contesteffects))
target         | The type of target that will recieve the effects of the attack                                                                                                            | [MoveTarget](#movetargets)
type           | The elemental type of this move                                                                                                                                           | [Type](#types)

#### ContestComboSets

Name | Description | Data Type
---- | ----------- | ---------
normal | A detail of moves this move can be used before or after, granting additional appeal points in contests       | [[ContestComboDetail](#contestcombodetail)]
super  | A detail of moves this move can be used before or after, granting additional appeal points in super contests | [[ContestComboDetail](#contestcombodetail)]

#### ContestComboDetail

Name | Description | Data Type
---- | ----------- | ---------
use_before | A list of moves to use before this move | [[APIReference](#apireference) ([Move](#moves))]
use_after  | A list of moves to use after this move  | [[APIReference](#apireference) ([Move](#moves))]

#### MoveMetaData

Name | Description | Data Type
---- | ----------- | ---------
ailment        | The status ailment this move inflicts on its target                                                    | [APIReference](#apireference) ([MoveAilment](#moveailments))
category       | The category of move this move falls under, e.g. damage or ailment                                     | [APIReference](#apireference) ([Move](#moves))
min_hits       | The minimum number of times this move hits. Null if it always only hits once.                          | integer
max_hits       | The maximum number of times this move hits. Null if it always only hits once.                          | integer
min_turns      | The minimum number of turns this move continues to take effect. Null if it always only lasts one turn. | integer
max_turns      | The maximum number of turns this move continues to take effect. Null if it always only lasts one turn. | integer
drain          | HP drain (if positive) or Recoil damage (if negative), in percent of damage done                       | integer
healing        | The amount of hp gained by the attacking pokemon, in percent of it's maximum HP                        | integer
crit_rate      | Critical hit rate bonus                                                                                | integer
ailment_chance | The likelyhood this attack will cause an ailment                                                       | integer
flinch_chance  | The likelyhood this attack will cause the target pokemon to flinch                                     | integer
stat_chance    | The likelyhood this attack will cause a stat change in the target pokemon                              | integer

#### MoveStatChange

Name | Description | Data Type
---- | ----------- | ---------
change | The amount of change    | integer
stat   | The stat being affected | [APIReference](#apireference) [Stat](#stats)

#### PastMoveStatValues

Name | Description | Data Type
---- | ----------- | ---------
accuracy       | The percent value of how likely this move is to be successful                  | integer
effect_chance  | The percent value of how likely it is this moves effect will take effect       | integer
power          | The base power of this move with a value of 0 if it does not have a base power | integer
pp             | Power points. The number of times this move can be used                        | integer
effect_entries | The effect of this move listed in different languages                          | [[VerboseEffect](#verboseeffect)]
type           | The elemental type of this move                                                | [Type](#types)
version group  | The version group in which these move stat values were in effect               | [APIReference](#apireference) [VersionGroup](#versiongroups)


## Move Ailments
```
api/v2/move-ailment/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id    | The identifier for this move ailment resource               | integer
name  | The name for this move ailment resource	                    | string
moves | A list of moves that cause this ailment                     | [[APIReference](#apireference) ([Move](#moves))]
names | The name of this move ailment listed in different languages | [[Name](#resourcename)]


## Move Battle Style
```
api/v2/move-battle-style/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id    | The identifier for this move battle style resource               | integer
name  | The name for this move battle style resource                     | string
names | The name of this move battle style listed in different languages | [[Name](#resourcename)]


## Move Category
```
api/v2/move-category/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id           | The identifier for this move category resource                     | integer
name         | The name for this move category resource	                          | string
moves        | A list of moves that fall into this category                       | [[APIReference](#apireference) ([Move](#moves))]
descriptions | The description of this move ailment listed in different languages | [[Description](#description)]


## Move Damage Class
```
api/v2/move-damage-class/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id           | The identifier for this move damage class resource                      | integer
name         | The name for this move damage class resource	                           | string
descriptions | The description of this move damage class listed in different languages | [[Description](#description)]
moves        | A list of moves that fall into this damage class                        | [[APIReference](#apireference) ([Move](#moves))]
names        | The name of this move damage class listed in different languages        | [[Name](#resourcename)]


## Move Learn Mathod
```
api/v2/move-learn-method/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id             | The identifier for this move learn method resource                      | integer
name           | The name for this move learn method resource                            | string
descriptions   | The description of this move learn method listed in different languages | [[Description](#description)]
names          | The name of this move learn method listed in different languages        | [[Name](#resourcename)]
version_groups | A list of version groups where moves can be learned through this method | [[APIReference](#apireference) ([VersionGroup](#versiongroups))]


## Move Target
```
api/v2/move-target/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id           | The identifier for this move target resource                      | integer
name         | The name for this move target resource                            | string
descriptions | The description of this move target listed in different languages | [[Description](#description)]
moves        | A list of moves that that are directed at this target             | [[APIReference](#apireference) ([Move](#moves))]
names        | The name of this move target listed in different languages        | [[Name](#resourcename)]


## Nature
```
api/v2/nature/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id                            | The identifier for this nature resource                                                                               | integer
name                          | The name for this nature resource                                                                                     | string
decreased_stat                | The stat decreased by 10% in pokemon with this nature                                                                 | [APIReference](#apireference) ([Stat](#stats)
increased_stat                | The stat increased by 10% in pokemon with this nature                                                                 | [APIReference](#apireference) ([Stat](#stats)
hates_flavor                  | The flavor hated by pokemon with this nature                                                                          | [APIReference](#apireference) ([BerryFlavor](#berryflavors)
likes_flavor                  | The flavor liked by pokemon with this nature                                                                          | [APIReference](#apireference) ([BerryFlavor](#berryflavors)
pokeathlon_stat_changes       | A list of pokeathlon stats this nature effects and how much it effects them                                           | [[NatureStatChange](#naturestatchange)]
move_battle_style_preferences | A list of battle styles and how likely a pokemon with this nature is to use them in the Battle Palace or Battle Tent. | [[MoveBattleStylePreference](#movebattlestylepreference)]
names                         | The name of this nature listed in different languages                                                                 | [[Name](#resourcename)]

#### NatureStatChange

Name | Description | Data Type
---- | ----------- | ---------
change | The amount of change    | integer
stat   | The stat being affected | [APIReference](#apireference) ([PokeathlonStat](#pokeathlonstats))

#### MoveBattleStylePreference

Name | Description | Data Type
---- | ----------- | ---------
low_hp_preference  | Chance of using the move, in percent, if HP is under one half | integer
high_hp_preference | Chance of using the move, in percent, if HP is over one half  | integer
move_battle_style  | The move battle style                                         | [APIReference](#apireference) ([MoveBattleStyle](#movebattlestyles))


## PalParkArea
```
api/v2/pal-park-area/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id                 | The identifier for this pal park area resource                        | integer
name               | The name for this pal park area resource                              | string
names              | The name of this pal park area listed in different languages          | [[Name](#resourcename)]
pokemon_encounters | A list of pokemon encountered in thi pal park area along with details | [PalParkEncounterSpecies](#palparkencounterspecies)

#### PalParkEncounterSpecies

Name | Description | Data Type
---- | ----------- | ---------
base_score      | The base score given to the player when this pokemon is caught during a pal park run | integer
rate            | The base rate for encountering this pokemon in this pal park area                    | integer
pokemon_species | The pokemon species being encountered                                                | [APIResource](#apiresource) ([PokemonSpecies](#pokemonspecies))


## Pokedex
```
api/v2/pokedex/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id              | The identifier for this pokedex resource                                     | integer
name            | The name for this pokedex resource                                           | string
is_main_series  | Whether or not this pokedex originated in the main series of the video games | boolean
descriptions    | The description of this pokedex listed in different languages                | [[Description](#description)]
names           | The name of this pokedex listed in different languages                       | [[Name](#resourcename)]
pokemon_entries | A list of pokemon catalogued in this pokedex and their indexes               | [[PokemonEntry](#pokemonentry)]
region          | The region this pokedex catalogues pokemon for                               | [APIReference](#apireference) ([Region](#regions))
version_groups  | A list of version groups this pokedex is relevent to                         | [APIReference](#apireference) ([VersionGroup](#versiongroups))

#### PalParkEncounter

Name | Description | Data Type
---- | ----------- | ---------
entry_number    | The index of this pokemon species entry within the pokedex | integer
pokemon_species | The pokemon species being encountered                      | [APIResource](#apiresource) ([PokemonSpecies](#pokemonspecies))


## Pokemon
```
api/v2/pokemon/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id                       | The identifier for this pokemon resource                         | integer
name                     | The name for this pokemon resource                               | string
base_experience          | The base experience gained for defeating this pokemon            | integer
height                   | The height of this pokemon                                       | integer
is_default               | Set for exactly one pokemon used as the default for each species | boolean
order                    | TODO                                                             | integer
weight                   | The weight of this pokemon                                       | integer
abilities                | A list of abilities this pokemon could potentially have          | [[PokemonAbility](#pokemonability)]
forms                    | A list of forms this pokemon can take on                         | [[APIResource](#apiresource) ([PokemonForm](#pokemonforms))]
game_indices             | A list of game indices relevent to pokemon item by generation    | [[VersionGameIndex](#versiongameindex)]
held_items               | A list of items this pokemon may be holding when encountered     | [[APIResource](#apiresource) ([Item](#items))]
location_area_encounters |
moves                    |
species                  | The species this pokemon belongs to                              | [PokemonSpecies](#pokemonspecies))
stats                    | A list of base stat values for this pokemon                      | [[APIResource](#apiresource) ([Stat](#stats))]
types                    | A list of details showing types this pokemon has                 | [([PokemonType](#pokemontype))]

#### PokemonAbility

Name | Description | Data Type
---- | ----------- | ---------
is_hidden | Whether or not this is a hidden ability                | boolean
slot      | The slot this ability occupies in this pokemon species | integer
ability   | The ability the pokemon may have                       | [APIResource](#apiresource) ([Ability](#abilities))

#### PokemonType

Name | Description | Data Type
---- | ----------- | ---------
slot | The order the pokemons types are listed in | integer
type | The type the referenced pokemon has        | string

## Pokemon Colors
```
api/v2/pokemon-color/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id              | The identifier for this pokemon color resource               | integer
name            | The name for this pokemon color resource                     | string
names           | The name of this pokemon color listed in different languages | [[Name](#resourcename)]
pokemon_species | A list of the pokemon species that have this color           | [[APIResource](#apiresource) ([PokemonSpecies](#pokemonspecies))]


## Pokemon Forms
```
api/v2/pokemon-form/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id             | The identifier for this pokemon color resource                                                                                                            | integer
name           | The name for this pokemon color resource                                                                                                                  | string
order          | The order in which forms should be sorted within all forms.  Multiple forms may have equal order, in which case they should fall back on sorting by name. | integer
form_order     | The order in which forms should be sorted within a species' forms                                                                                         | integer
is_default     | True for exactly one form used as the default for each pokemon                                                                                            | boolean
is_battle_only | Whether or not this form can only happen during battle                                                                                                    | boolean
is_mega        | Whether or not this form requires mega evolution                                                                                                          | boolean
form_name      | The name of this form                                                                                                                                     | string
pokemon        | The pokemon that can take on this form                                                                                                                    | [APIResource](#apiresource) ([Pokemon](#pokemon))
version_group  | The version group this pokemon form was introduced in                                                                                                     | [APIResource](#apiresource) ([VersionGroup](#versiongroups))


## Pokemon Habitats
```
api/v2/pokemon-habitat/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id              | The identifier for this pokemon habitat resource                | integer
name            | The name for this pokemon habitat resource                      | string
names           | The name of this pokemon habitat listed in different languages  | [[Name](#resourcename)]
pokemon_species | A list of the pokemon species that can be found in this habitat | [[APIResource](#apiresource) ([PokemonSpecies](#pokemonspecies))]


## Pokemon Shapes
```
api/v2/pokemon-shape/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id              | The identifier for this pokemon shape resource                            | integer
name            | The name for this pokemon shape resource                                  | string
awesome_names   | The "scientific" name of this pokemon shape listed in different languages | [[AwesomeName](#awesomename)]
names           | The name of this pokemon shape listed in different languages              | [[Name](#resourcename)]
pokemon_species | A list of the pokemon species that have this shape                        | [[APIResource](#apiresource) ([PokemonSpecies](#pokemonspecies))]

#### AwesomeName

Name | Description | Data Type
---- | ----------- | ---------
awesome_name | The localized "scientific" name for an api resource in a specific language | string
language     | The language this "scientific" name is in                                  | [APIResource](#apiresource) ([Language](#languages))


## Pokemon Species
```
api/v2/pokemon-species/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id                     | The identifier for this pokemon species resource                                                                                                   | integer
name                   | The name for this pokemon species resource                                                                                                         | string
order                  | The order in which species should be sorted.  Based on National Dex order, except families are grouped together and sorted by stage.               | integer
gender_rate            | The chance of this Pokémon being female, in eighths; or -1 for genderless                                                                          | integer
capture_rate           | The base capture rate; up to 255. The higher the number, the easier the catch.                                                                     | integer
base_happiness         | The happiness when caught by a normal pokeball; up to 255. The higher the number, the happier the pokemon.                                         | integer
is_baby                | Whether or not this is a baby pokemon                                                                                                              | boolean
hatch_counter          | Initial hatch counter: one must walk 255 × (hatch_counter + 1) steps before this Pokémon's egg hatches, unless utilizing bonuses like Flame Body's | integer
has_gender_differences | Whether or not this pokemon can have different genders                                                                                             | boolean
forms_switchable       | Whether or not this pokemon has multiple forms and can switch between them                                                                         | boolean
growth_rate            | The rate at which this pokemon species gains levels                                                                                                | [APIResource](#apiresource) ([GrowthRate](#growthrates))
pokedex_numbers        | A list of pokedexes and the indexes reserved within them for this pokemon species                                                                  | [PokemonSpeciesDexEntry](#pokemonspeciesdexentry)
egg_groups             | A list of egg groups this pokemon species is a member of                                                                                           | [[APIResource](#apiresource) ([EggGroup](#egggroups))]
color                  | The color of this pokemon for gimmicky pokedex search                                                                                              | [[APIResource](#apiresource) ([PokemonColor](#pokemoncolors))]
shape                  | The shape of this pokemon for gimmicky pokedex search                                                                                              | [[APIResource](#apiresource) ([PokemonShape](#pokemonshapes))]
evolves_from_species   | The pokemon species that evolves into this pokemon_species                                                                                         | [APIResource](#apiresource) ([PokemonSpecies](#pokemonspecies))
evolution_chain        | The evolution chain this pokemon species is a member of                                                                                            | [APIResource](#apiresource) ([EvolutionChain](#evolutionchains))
habitat                | The habitat this pokemon species can be encountered in                                                                                             | [APIResource](#apiresource) ([PokemonHabitat](#pokemonhabitats))
generation             | The generation this pokemon species was introduced in                                                                                              | [APIResource](#apiresource) ([Generation](#generations))
names                  | The name of this pokemon species listed in different languages                                                                                     | [[Name](#resourcename)]
pal_park_encounters    | A list of encounters that can be had with this pokemon species in pal park                                                                         | [[PalParkEncounterArea](#palparkencounterarea)]
form_descriptions      | TODO
genera                 | The genus of this pokemon species listed in multiple languages                                                                                     | [Genus](#genus)
varieties              | A list of the pokemon that exist within this pokemon species                                                                                       | [[APIResource](#apiresource) ([Pokemon](#pokemon))]

#### Genus

Name | Description | Data Type
---- | ----------- | ---------
genus    | The localized genus for the referenced pokemon species | string
language | The language this genus is in                          | [APIResource](#apiresource) ([Language](#languages))

####PokemonSpeciesDexEntry

Name | Description | Data Type
---- | ----------- | ---------
entry_number | The index number within the pokedex                       | integer
name         | The pokdex the referenced pokemon species can be found in | [APIResource](#apiresource) ([Pokedex](#pokedexes))

####PalParkEncounterArea

Name | Description | Data Type
---- | ----------- | ---------
base_score | The base score given to the player when the referenced pokemon is caught during a pal park run | integer
rate       | The base rate for encountering the referenced pokemon in this pal park area                    | integer
area       | The pal park area where this encounter happens                                                 | [APIResource](#apiresource) ([PalParkArea](#palparkareas))


## Pokeathlon Stat
```
api/v2/pokeathlon-stat/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id                | The identifier for this pokeathlon stat resource                    | integer
name              | The name for this pokeathlon stat resource                          | string
names             | The name of this pokeathlon stat listed in different languages      | [[Name](#resourcename)]
affecting_natures | A detail of natures which affect this pokeathlon stat positively or negatively | [NaturePokeathlonStatAffectSets](#naturepokeathlonstataffectsets)

#### NaturePokeathlonStatAffectSets

Name | Description | Data Type
---- | ----------- | ---------
increase | A list of natures and how they change the referenced pokeathlon stat | [NaturePokeathlonStatAffect](#naturepokeathlonstataffect)
decrease | A list of natures and how they change the referenced pokeathlon stat | [NaturePokeathlonStatAffect](#naturepokeathlonstataffect)

####NaturePokeathlonStatAffect

Name | Description | Data Type
---- | ----------- | ---------
max_change | The maximum amount of change to the referenced pokeathlon stat | integer
nature     | The nature causing the change                                  | [APIResource](#apiresource) ([Nature](#natures))


## Region
```
api/v2/region/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id              | The identifier for this region resource                   | integer
name            | The name for this region resource                         | string
locations       | A list of locations that can be found in this region      | [APIResource](#apiresource) ([Location](#locations))
main_generation | The generation this region was introduced in              | [APIResource](#apiresource) ([Generation](#generations))
names           | The name of this region listed in different languages     | [[Name](#resourcename)]
pokedexes       | A list of pokedexes that catalogue pokemon in this region | [APIResource](#apiresource) ([Pokedex](#pokedexes))
version_groups  | A list of version groups where this region can be visited | [APIResource](#apiresource) ([VersionGroup](#versiongroups))


## Stats
```
api/v2/stat/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id                | The identifier for this stat resource                                                       | integer
name              | The name for this stat resource                                                             | string
game_index        | ID the games use for this stat                                                              | integer
is_battle_only    | Whether this stat only exists within a battle                                               | boolean
affecting_moves   | A detail of moves which affect this stat positively or negatively                           | [MoveStatAffectSets](#movestataffectsets)
affecting_natures | A detail of natures which affect this stat positively or negatively                         | [NatureStatAffectSets](#naturestataffectsets)
characteristics   | A list of characteristics that are set on a pokemon when its highest base stat is this stat | [[APIResource](#apiresource) ([Characteristic](#characteristics))]
move_damage_class | The class of damage this stat is directly related to                                        | [APIResource](#apiresource) ([MoveDamageClass](#movedamageclasses))
names             | The name of this region listed in different languages                                       | [[Name](#resourcename)]

#### MoveStatAffectSets

Name | Description | Data Type
---- | ----------- | ---------
increase | A list of moves and how they change the referenced stat | [MoveStatAffect](#movestataffect)
decrease | A list of moves and how they change the referenced stat | [MoveStatAffect](#movestataffect)

#### MoveStatAffect

Name | Description | Data Type
---- | ----------- | ---------
max_change | The maximum amount of change to the referenced stat | integer
move       | The move causing the change                         | [APIResource](#apiresource) ([Move](#moves))

#### NatureStatAffectSets

Name | Description | Data Type
---- | ----------- | ---------
increase | A list of natures and how they change the referenced stat | [NatureStatAffect](#naturestataffect)
decrease | A list of nature sand how they change the referenced stat | [NatureStatAffect](#naturestataffect)

#### NatureStatAffect

Name | Description | Data Type
---- | ----------- | ---------
max_change | The maximum amount of change to the referenced stat | integer
nature     | The nature causing the change                       | [APIResource](#apiresource) ([Nature](#natures))


## Super Contest Effects
```
api/v2/super-contest-effect/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id                  | The identifier for this super contest effect resource                      | integer
appeal              | The level of appeal this super contest effect has                          | string
flavor_text_entries | The flavor text of this super contest effect listed in different languages | [[FlavorText](#flavortext)]
moves               | A list of moves that have the effect when used in super contests           | [[APIResource](#apiresource) ([Move](#moves))]


## Types
```
api/v2/types/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id                | The identifier for this type resource                      | integer
name              | The name for this type resource                            | string
damage_relations  |
game_indices      | A list of game indices relevent to this item by generation | [[GenerationGameIndex](#generationgameindex)]
generation        | The generation this type was introduced in                 | [APIResource](#apiresource) ([Generation](#generations)
move_damage_class | The class of damage inflicted by this type                 | [APIResource](#apiresource) ([MoveDamageClass](#movedamageclasses))
names             | The name of this type listed in different languages        | [[Name](#resourcename)]
pokemon           | A list of details of pokemon that have this type           | [TypePokemon](#typepokemon)
moves             | A list of moves that have this type                        | [[APIResource](#apiresource) ([Move](#moves))]

#### TypePokemon

Name | Description | Data Type
---- | ----------- | ---------
slot    | The order the pokemons types are listed in | integer
pokemon | The pokemon that has the referenced type   | [APIResource](#apiresource) ([Pokemon](#pokemon)


## Versions
```
api/v2/version/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id            | The identifier for this version resource               | integer
name          | The name for this version resource                     | string
names         | The name of this version listed in different languages | [[Name](#resourcename)]
version_group | The version group this version belongs to              | [[APIResource](#apiresource) ([VersionGroup](#versiongroups))]


## Version Groups
```
api/v2/version-group/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id                 | The identifier for this version group resource                                              | integer
name               | The name for this version group resource                                                    | string
order              | Order for sorting. Almost by date of release, except similar versions are grouped together. | integer
generation         | The generation this version was introduced in                                               | [[APIResource](#apiresource) ([Generation](#generations))]
move_learn_methods | A list of methods in which pokemon can learn moves in this version group                    | [[APIResource](#apiresource) ([MoveLearnMethod](#mofelearnmethods))]
names              | The name of this version group listed in different languages                                | [[Name](#resourcename)]
pokedexes          | A list of pokedexes introduces in this version group                                        | [[APIResource](#apiresource) ([Pokedex](#pokedexes))]
regions            | A list of regions that can be visited in this version group                                 | [[APIResource](#apiresource) ([Region](#regions))]
versions           | The versions this version group owns                                                        | [[APIResource](#apiresource) ([Version](#versions))]



## Common Models

#### APIResource

Name | Description | Data Type
---- | ----------- | ---------
name | The name of the referenced resource | string
url  | The url of the referenced resource  | string


#### Description

Name | Description | Data Type
---- | ----------- | ---------
description | The localized description for an api resource in a specific language | string
language    | The language this name is in                                         | [APIResource](#apiresource) ([Language](#languages))


#### Effect

Name | Description | Data Type
---- | ----------- | ---------
effect   | The localized effect text for an api resource in a specific language | string
language | The language this effect is in                                       | [APIResource](#apiresource) ([Language](#language))


#### Encounter

Name | Description | Data Type
---- | ----------- | ---------
min_level        | The lowest level the pokemon could be encountered at                          | integer
max_level        | The highest level the pokemon could be encountered at                         | integer
condition_values | A list of condition values that must be in effect for this encounter to occur | [[APIResource](#apiresource) ([EncounterConditionValue](#encounterconditionvalue))]
chance           | percent chance that this encounter will occur                                 | integer
method           | The method by which this encounter happens                                    | [APIResource](#apiresource) ([EncounterMethod](#encountermethod))


#### FlavorText

Name | Description | Data Type
---- | ----------- | ---------
flavor_text | The localized name for an api resource in a specific language | string
language    | The language this name is in                                  | [APIResource](#apiresource) ([Language](#language))


#### GenerationGameIndex

Name       | Description                                         | Data Type
----       | -----------                                         | ---------
game_index | The internal id of an api resource within game data | integer
generation | The generation relevent to this game index          | [APIResource](#apiresource) ([Generation](#generation))


#### <a name="resourcename"></a>Name

Name | Description | Data Type
---- | ----------- | ---------
name     | The localized name for an api resource in a specific language | string
language | The language this name is in                                  | [APIResource](#apiresource) ([Language](#language))


#### VerboseEffect

Name | Description | Data Type
---- | ----------- | ---------
effect       | The localized effect text for an api resource in a specific language | string
short_effect | The localized effect text in brief                                   | string
language     | The language this effect is in                                       | [APIResource](#apiresource) ([Language](#language))


#### VersionGameIndex

Name       | Description                                         | Data Type
----       | -----------                                         | ---------
game_index | The internal id of an api resource within game data | integer
version    | The version relevent to this game index             | [APIResource](#apiresource) ([Version](#version))


#### VersionSpecificFlavorText TODO

Name | Description | Data Type
---- | ----------- | ---------
flavor_text | The localized name for an api resource in a specific language | string
language    | The language this name is in                                  | [APIResource](#apiresource) ([Language](#language))









