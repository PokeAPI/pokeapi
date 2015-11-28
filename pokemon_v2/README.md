# Pokeapi V2 API Reference



### Abilities
---
GET `api/v2/ability/{id or name}`

Abilities provide passive effects for pokemon in battle or overworld. Pokemon can have only one ability at a time.

Name | Description | Data Type
---- | ----------- | ---------
id                  | The identifier for this ability resource                                                                                                 | integer
name                | The name for this ability resource                                                                                                       | string
is_main_series      | Whether or not this ability originated in the main series of the video games                                                             | boolean
generation          | The generation this ability originated in                                                                                                | [APIResource](#apiresource)([Generation](#generation))
names               | The name of this ability listed in different languages                                                                                   | [[Name](#resourcename)]
effect_entries      | The effect of this ability listed in different languages                                                                                 | [[VerboseEffect](#verboseeffect)]
effect_changes      | Some abilities effects have changed across different version groups of the games. This is a list of those changes in different languages | [[AbilityEffectChange](#abilityeffectchange)]
flavor_text_entries | The flavor text of this ability listed in different languages                                                                            | [VersionSpecificFlavorText] TODO
pokemon             | A list of pokemon that could potentially have this ability                                                                               | [[AbilityPokemonMap](#abilitypokemonmap)]

##### AbilityEffectChange

Name | Description | Data Type
---- | ----------- | ---------
effect_entries | The previous effect of this ability listed in different languages         | [Effect]
version_group  | The version group in which the previous effect of this ability originated | APIReference

##### AbilityPokemonMap

Name | Description | Data Type
---- | ----------- | ---------
is_hidden | Whether or not this a hidden ability for the referenced pokemon                                                                                          | boolean
slot      | Pokemon have 3 ability 'slots' which hold references to possible abilities they could have. This is the slot of this ability for the referenced pokemon. | integer
pokemon   | The pokemon this ability could belong to                                                                                                                 | APIReference



### Berries
---
```
api/v2/berry/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id                 | The identifier for this berry resource | integer
name               | The name for this berry resource | string
growth_time        | TODO | integer
max_harvest        | TODO | integer
natural_gift_power | The strength of this powers natural gift | integer
size               | The size of this berry | integer
smoothness         | The smoothness rating of this berry | integer
soil_dryness       | TODO | integer
firmness           | The firmness of this berry | APIReference
flavors            | A list of references to each flavor a berry can have and the potency of each of those flavors in regard to this berry | [BerryFlavorMap]
item               | Berries are actually items. This is a reference to the item specific data for this berry. | APIReference
natural_gift_type  | A reference to the elemental type of a this berry TODO | APIReference

#### BerryFlavorMap

Name | Description | Data Type
---- | ----------- | ---------
potency | How powerful the referenced flavor is for this berry | integer
flavor  | The referenced berry flavor | APIReference



### Berry Firmnesses
---
```
api/v2/berry-firmness/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id      | The identifier for this berry firmness resource | integer
name    | The name for this berry firmness resource | string
berries | A list of the berries with this firmness | [APIReference]
names   | The name of this berry firmness listed in different languages | [Name]



### Berry Flavors
---
```
api/v2/berry-flavor/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id           | The identifier for this berry flavor resource | integer
name         | The name for this berry flavor resource | string
berries      | A list of the berries with this flavor | [APIReference]
contest_type | TODO | APIReference
names        | The name of this berry flavor listed in different languages | [Name]
 


### Characteristics
---
```
api/v2/characteristic/{id}
```

Name | Description | Data Type
---- | ----------- | ---------
id              | The identifier for this characteristic resource | integer
gene_modulo     | The remainder of the highest stat divided by 5 TODO | integer
possible_values | The possible values of the highest stat that would result in a pokemon recieving this characteristic when divided by the gene modulo | [integer]
descriptions    | The descriptions of this characteristic listed in different languages | [Description]



### Contest Type
---
```
api/v2/contest-type/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id           | The identifier for this contest type resource | integer
name         | The name for this contest type resource | string
berry_flavor | TODO | APIReference
names        | The name of this contest type listed in different languages | [Name]



### Contest Effect
---
```
api/v2/contest-effect/{id}
```

Name | Description | Data Type
---- | ----------- | ---------
id                  | The identifier for this contest type resource | integer
appeal              | The level of appeal this effect has TODO | string
jam                 | TODO | APIReference
effect_entries      | The result of this contest effect listed in different languages | [Effect]
flavor_text_entries | The flavor text of this contest effect listed in different languages | [FlavorText]



### Egg Group
---
```
api/v2/egg-group/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id              | The identifier for this egg group resource | integer
name            | The name for this egg group resource | string
names           | The name of this egg group listed in different languages | [Name]
pokemon_species | A list of all pokemon species that are categorized under this egg group



### Encounter Method
---
```
api/v2/encounter-method/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id    | The identifier for this encounter method resource | integer
name  | The name for this encounter method resource | string
order | The order index of this encounter method within the main game series data | integer
names | The name of this encounter method listed in different languages | [Name]



### Encounter Conditions
---
```
api/v2/encounter-condition/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id     | The identifier for this encounter condition resource | integer
name   | The name for this encounter condition resource | string
names  | The name of this encounter method listed in different languages | [Name]
values | A list of possible values for this encounter condition | [APIReference]



### Encounter Condition Values TODO (These should probably be renamed "states")
---
```
api/v2/encounter-condition-value/{id or name}
```

Name | Description | Data Type
---- | ----------- | ---------
id        | The identifier for this encounter condition value resource | integer
name      | The name for this encounter condition value resource | string
condition | The condition this encounter condition value pertains to | [APIReference]
names     | The name of this encounter method listed in different languages | [Name]



### Evolution Chain
---
```
api/v2/encounter-chain/{id}
```

Name | Description | Data Type
---- | ----------- | ---------
id                | The identifier for this evolution chain resource | integer
baby_trigger_item | The item that a pokemon would be holding when mating that would trigger the egg hatching a baby pokemon rather than a basic pokemon | APIReference
chain             | The base link object. Each link contains evolution details for a pokemon in the chain. Each link references the next pokemon in the natural evolution order.  | Link


#### Chain

Name | Description | Data Type
---- | ----------- | ---------
is_baby           | Whether or not this link is for a baby pokemon. This would only ever be true on the base link. | boolean
species           | The pokemon species at this point in the evolution chain | APIReference
evolution_details | All details regarding 
evolves_to        | A List of chain objects. These contain details of the species this pokemon species evolves into



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
language    | The language this name is in | APIResource


#### Effect

Name | Description | Data Type
---- | ----------- | ---------
effect       | The localized effect text for an api resource in a specific language  | string
language     | The language this effect is in | APIResource


#### FlavorText

Name | Description | Data Type
---- | ----------- | ---------
flavor_text | The localized name for an api resource in a specific language | string
language    | The language this name is in | APIResource


#### <a name="resourcename"></a>Name

Name | Description | Data Type
---- | ----------- | ---------
name     | The localized name for an api resource in a specific language | string
language | The language this name is in | APIResource


#### VerboseEffect

Name | Description | Data Type
---- | ----------- | ---------
effect       | The localized effect text for an api resource in a specific language  | string
short_effect | The localized effect text in brief | string
language     | The language this effect is in | APIResource


#### VersionSpecificFlavorText TODO

Name | Description | Data Type
---- | ----------- | ---------
flavor_text | The localized name for an api resource in a specific language | string
language    | The language this name is in | APIResource