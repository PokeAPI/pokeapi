# Pokeapi V2 API Reference



## Abilities
```
api/v2/ability/{id or name}
```
Abilities provide passive effects for pokemon in battle or overworld. Pokemon can have only one ability at a time. Check out [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Ability) for greater detail.

Name | Description | Data Type
---- | ----------- | ---------
id                  | The identifier for this ability resource                                                                                                 | integer
name                | The name for this ability resource                                                                                                       | string
is_main_series      | Whether or not this ability originated in the main series of the video games                                                             | boolean
generation          | The generation this ability originated in                                                                                                | [APIResource](#apiresource) ([Generation](#generation))
names               | The name of this ability listed in different languages                                                                                   | [[Name](#resourcename)]
effect_entries      | The effect of this ability listed in different languages                                                                                 | [[VerboseEffect](#verboseeffect)]
effect_changes      | Some abilities effects have changed across different version groups of the games. This is a list of those changes in different languages | [[AbilityEffectChange](#abilityeffectchange)]
flavor_text_entries | The flavor text of this ability listed in different languages                                                                            | [VersionSpecificFlavorText] TODO
pokemon             | A list of pokemon that could potentially have this ability                                                                               | [[AbilityPokemonMap](#abilitypokemonmap)]

#### AbilityEffectChange

Name | Description | Data Type
---- | ----------- | ---------
effect_entries | The previous effect of this ability listed in different languages         | [Effect]
version_group  | The version group in which the previous effect of this ability originated | [APIResource](#apiresource) ([VersionGroup](#versiongroup))

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
firmness           | The firmness of this berry                                                                                            | [APIResource](#apiresource) ([BerryFirmness](#berryfirmness))
flavors            | A list of references to each flavor a berry can have and the potency of each of those flavors in regard to this berry | [[BerryFlavorMap](#berryflavormap)]
item               | Berries are actually items. This is a reference to the item specific data for this berry.                             | [APIResource](#apiresource) ([Item](#item))
natural_gift_type  | A reference to the elemental type of a this berry TODO                                                                | [APIResource](#apiresource) ([Type](#type))

#### BerryFlavorMap

Name | Description | Data Type
---- | ----------- | ---------
potency | How powerful the referenced flavor is for this berry | integer
flavor  | The referenced berry flavor                          | [APIResource](#apiresource) ([BerryFlavor](#berryflavor))



## Berry Firmnesses
```
api/v2/berry-firmness/{id or name}
```
TODO. Absolutely no idea what firmness does for a berry. Check out [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Berry) for greater detail.

Name | Description | Data Type
---- | ----------- | ---------
id      | The identifier for this berry firmness resource               | integer
name    | The name for this berry firmness resource                     | string
berries | A list of the berries with this firmness                      | [[APIResource](#apiresource) ([Berry](#berry))]
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
berries      | A list of the berries with this flavor                      | [[APIResource](#apiresource) ([Berry](#berry))]
contest_type | TODO                                                        | [APIResource](#apiresource) ([ContestType](#contesttype))
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
berry_flavor | TODO                                                        | [APIResource](#apiresource) ([BerryFlavor](#berryflavor))
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



## Evolution Chain
```
api/v2/evolution-chain/{id}
```

Name | Description | Data Type
---- | ----------- | ---------
id                | The identifier for this evolution chain resource                                                                                                                   | integer
baby_trigger_item | The item that a pokemon would be holding when mating that would trigger the egg hatching a baby pokemon rather than a basic pokemon                                | [APIReference](#apireference)
chain             | The base chain link object. Each link contains evolution details for a pokemon in the chain. Each link references the next pokemon in the natural evolution order. | [ChainLink](#chainlink)

#### Chain Link

Name | Description | Data Type
---- | ----------- | ---------
is_baby           | Whether or not this link is for a baby pokemon. This would only ever be true on the base link. | boolean
species           | The pokemon species at this point in the evolution chain                                       | [APIReference](#apireference)
evolution_details | All details regarding the specific details of the referenced pokemon species evolution         | [APIReference](#apireference) ([EvolutionDetail](#evolutiondetail))
evolves_to        | A List of chain objects.                                                                       | [ChainLink](#chainlink)

#### Evolution Detail

Name | Description | Data Type
---- | ----------- | ---------
item                    | The item required to cause evolution this into pokemon species                                                                                                              | [APIReference](#apireference) ([Item](#item))
trigger                 | The type of event that triggers evolution into this pokemon species                                                                                                         | [APIReference](#apireference) ([EvolutionTrigger](#evolutiontrigger))
gender                  | The gender the evolving pokemon species must be in order to evolve into this pokemon species                                                                                | [APIReference](#apireference) ([Gender](#gender))
held_item               | The item the evolving pokemon species must be holding during the evolution trigger event to evolve into this pokemon species                                                | [APIReference](#apireference) ([Item](#item))
known_move              | The move that must be known by the evolving pokemon species during the evolution trigger event in order to evolve into this pokemon species                                 | [APIReference](#apireference) ([Move](#move))
known_move_type         | The evolving pokemon species must know a move with this type during the evolution trigger event in order to evolve into this pokemon species                                | [APIReference](#apireference) ([Type](#type))
location                | The location the evolution must be triggered at.                                                            | [APIReference](#apireference) ([Location](#location))
min_level               | The minimum required level of the evolving pokemon species to evolve into this pokemon species                                                                                  | integer
min_hapiness            | The minimum required level of happiness the evolving pokemon species to evolve into this pokemon species                                                                   | integer
min_beauty              | The minimum required level of beauty the evolving pokemon species to evolve into this pokemon species                                                                      | integer
min_affection           | The minimum required level of affection the evolving pokemon species to evolve into this pokemon species                                                                   | integer
needs_overworld_rain    | Whether or not it must be raining in the overworld to cause evolution this pokemon species                                                                                  | boolean
party_species           | The pokemon species that must be in the players party in order for the evolving pokemon species to evolve into this pokemon species                                         | [APIReference](#apireference) ([PokemonSpecies](#pokemonspecies))
party_type              | The player must have a pokemon of this type in their party during the evolution trigger event in order for the evolving pokemon species to evolve into this pokemon species | [APIReference](#apireference) ([Type](#type))
relative_physical_stats | The required relation between the Pokémon's Attack and Defense stats. 1 means Attack > Defense. 0 means Attack = Defense. -1 means Attack < Defense.                        | integer
time_of_day             | The required time of day. Day or night.                                                                                                                                     | string
trade_species           | Pokemon species for which this one must be traded.                                                                                                                          | [APIReference](#apireference) ([Pokemon Species](#pokemonspecies))
turn_upside_down        | Whether or not the 3DS needs to be turned upside-down as this Pokémon levels up.                                                                                            | boolean


## Encounter Trigger
```
api/v2/evolution-trigger/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id              | The identifier for this evolution trigger resource                | integer
name            | The name for this evolution trigger resource                      | string
names           | The name of this evolution trigger listed in different languages  | [[Name](#resourcename)]
pokemon_species | A list of pokemon species that result from this evolution trigger | [[APIReference](#apireference) ([PokemonSpecies](#pokemonspecies))]


## Generation
```
api/v2/generation/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id              | The identifier for this generation resource                       | integer
name            | The name for this generation resource                             | string
abilities       | A list of abilities that were introduced in this generation       | [[APIReference](#apireference) ([Ability](#ability))]
names           | The name of this generation listed in different languages         | [[Name](#resourcename)]
main_region     | The main region travelled in this generation                      | [APIReference](#apireference) ([Region](#region))
moves           | A list of moves that were introduced in this generation           | [[APIReference](#apireference) ([Move](#move))]
pokemon_species | A list of pokemon species that were introduced in this generation | [[APIReference](#apireference) ([PokemonSpecies](#pokemonspecies))]
types           | A list of types that were introduced in this generation           | [[APIReference](#apireference) ([Type](#type))]
version_groups  | A list of version groups that were introduced in this generation  | [[APIReference](#apireference) ([VersionGroup](#versiongroup))]


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


## Growth Rate
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


## Item
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
attributes          | A list of attributes this item has                                   | [[APIReference](#apireference) ([ItemAttribute](#itemattribute))]
category            | The category of items this item falls into                           | [ItemCategory](#itemcategory)
effect_entries      | The effect of this ability listed in different languages             | [[VerboseEffect](#verboseeffect)]
flavor_text_entries | The flavor text of this ability listed in different languages        | [VersionSpecificFlavorText] TODO
game_indices        | A list of game indices relevent to this item by generation           | [[GenerationGameIndex](#generationgameindex)]
names               | The name of this item listed in different languages                  | [[Name](#resourcename)]
held_by_pokemon     | A list of pokemon that might be found in the wild holding this item  | [[APIReference](#apireference) ([Pokemon](#pokemon))]
baby_trigger_for    | An evolution chain this item requires to produce a bay during mating | [[APIReference](#apireference) ([Evolution Chain](#evolutionchain))]


## ItemFlingEffect
```
api/v2/item-fling-effect/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id             | The identifier for this fling effect resource                 | integer
name           | The name for this fling effect resource                       | string
effect_entries | The result of this fling effect listed in different languages | [[Effect](#effect)]
items          | A list of items that have this fling effect                   | [[Item](#item)]


## ItemCategory
```
api/v2/item-category/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id     | The identifier for this item category resource               | integer
name   | The name for this item category resource                     | string
items  | A list of items that fall into this category                 | [[Item](#item)]
names  | The name of this item category listed in different languages | [[Name](#resourcename)]
pocket | The pocket items in this category would be put in            | [[APIReference](#apireference) ([ItemPocket](#itempocket))]


## ItemPocket
```
api/v2/item-pocket/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id         | The identifier for this item pocket resource                    | integer
name       | The name for this item pocket resource                          | string
categories | A list of item categories that are relevent to this item pocket | [[ItemCategory](#itemcategory)]
names      | The name of this item category listed in different languages    | [[Name](#resourcename)]


## Language
```
api/v2/language/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id         | The identifier for this item pocket resource                    | integer
name       | The name for this item pocket resource                          | string



## Common Models

#### APIResource

Name | Description | Data Type
---- | ----------- | ---------
name | The name of the referenced resource | string
url  | The url of the referenced resource | string


#### Description

Name | Description | Data Type
---- | ----------- | ---------
description | The localized description for an api resource in a specific language | string
language    | The language this name is in | [APIResource](#apiresource) ([Language](#language))


#### Effect

Name | Description | Data Type
---- | ----------- | ---------
effect   | The localized effect text for an api resource in a specific language | string
language | The language this effect is in                                       | [APIResource](#apiresource) ([Language](#language))


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









